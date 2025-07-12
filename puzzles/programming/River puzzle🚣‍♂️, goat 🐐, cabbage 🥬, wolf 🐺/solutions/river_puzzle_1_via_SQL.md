# River Puzzle Database Architecture: A Rationalized Approach

This document outlines a refined database architecture for solving the classic River Crossing Puzzle (Human, Cabbage, Goat, Wolf). The goal of this design is to create a more flexible, scalable, and "rational" system where the database itself acts as the primary enforcer of puzzle constraints, making the solution highly transferable to other state-space search problems.

## Core Principles

1.  **Normalized State Representation:** Decouple the puzzle state from the specific elements, allowing for a variable number of elements without schema changes.
2.  **Database-Enforced Constraints:** Leverage SQL triggers to ensure that only valid puzzle states can ever be recorded in the database.
3.  **Clear Separation of Concerns:** The database manages the "rules of the game" and valid states, while the external solver (e.g., a Python script) focuses solely on exploring possible moves.

## Database Schema

### 1. `locations` Table

Defines the possible locations for all elements (e.g., river banks).

| Column      | Type    | Constraints      | Description             |
| :---------- | :------ | :--------------- | :---------------------- |
| `location_id` | `TEXT`  | `PRIMARY KEY`    | 'L' (Left) or 'R' (Right) |
| `description` | `TEXT`  |                  | Full name of the location |

### 2. `puzzle_elements` Table

(Retained from previous design) Defines the individual entities involved in the puzzle.

| Column    | Type      | Constraints   | Description             |
| :-------- | :-------- | :------------ | :---------------------- |
| `id`      | `INTEGER` | `PRIMARY KEY` | Unique ID for each element |
| `name`    | `TEXT`    | `UNIQUE`      | Name of the element (e.g., 'Human', 'Goat') |
| `type`    | `TEXT`    |               | Category (e.g., 'Agent', 'Item') |

### 3. `puzzle_states` Table

Represents a unique snapshot of the puzzle. This table is now simplified and does not directly store element locations.

| Column        | Type      | Constraints   | Description             |
| :------------ | :-------- | :------------ | :---------------------- |
| `state_id`    | `INTEGER` | `PRIMARY KEY`, `AUTOINCREMENT` | Unique ID for each puzzle state |
| `is_goal_state` | `INTEGER` | `NOT NULL`, `DEFAULT 0` | Flag (1 if all elements are on the 'R' bank, 0 otherwise) |

### 4. `state_element_locations` Table

This is the new, crucial table that links a `puzzle_state` to the specific location of each `puzzle_element` within that state. This provides the "X-dimensional" flexibility.

| Column        | Type      | Constraints   | Description             |
| :------------ | :-------- | :------------ | :---------------------- |
| `state_id`    | `INTEGER` | `NOT NULL`, `FOREIGN KEY` to `puzzle_states.state_id` | The state this location belongs to |
| `element_id`  | `INTEGER` | `NOT NULL`, `FOREIGN KEY` to `puzzle_elements.id` | The element whose location is being recorded |
| `location_id` | `TEXT`    | `NOT NULL`, `FOREIGN KEY` to `locations.location_id` | The location of the element in this state |
| `PRIMARY KEY (state_id, element_id)` |           |               | Ensures each element has only one location per state |
| `UNIQUE (state_id, element_id, location_id)` |           |               | Ensures no duplicate location entries for an element in a state |

### 5. `puzzle_transitions` Table

(Retained from previous design, but `from_state_id` and `to_state_id` now refer to the new `puzzle_states` table) Records valid moves between valid states.

| Column          | Type      | Constraints   | Description             |
| :-------------- | :-------- | :------------ | :---------------------- |
| `transition_id` | `INTEGER` | `PRIMARY KEY`, `AUTOINCREMENT` | Unique ID for each transition |
| `from_state_id` | `INTEGER` | `NOT NULL`, `FOREIGN KEY` to `puzzle_states.state_id` | The state before the move |
| `to_state_id`   | `INTEGER` | `NOT NULL`, `FOREIGN KEY` to `puzzle_states.state_id` | The state after the move |
| `item_carried_id` | `INTEGER` | `FOREIGN KEY` to `puzzle_elements.id` | The ID of the item carried (NULL if only human moves) |
| `direction`     | `TEXT`    | `NOT NULL`    | 'L_to_R' or 'R_to_L' |

## Constraint Enforcement: The `check_puzzle_state_validity` Trigger

This trigger is the core of the "law" enforcement. It would be defined on the `puzzle_states` table (or potentially on `state_element_locations` depending on the exact insertion flow) and would prevent the creation of any state that violates the puzzle's safety rules.

**Trigger Definition (Conceptual SQL for SQLite):**

```sql
CREATE TRIGGER check_puzzle_state_validity
BEFORE INSERT ON puzzle_states -- Or BEFORE INSERT ON state_element_locations, depending on transaction
FOR EACH ROW
BEGIN
    -- To check constraints, we need to know the locations of all elements
    -- in the NEW state being proposed. This would involve querying the
    -- state_element_locations table for the NEW.state_id.

    -- Example: Get locations for the NEW state
    -- (This logic would be more complex in a real trigger, potentially
    -- requiring a temporary view or careful subqueries to get all locations
    -- for the NEW.state_id before the full state is committed.)

    -- Let's assume we can access the locations for the NEW state_id:
    -- SELECT location_id FROM state_element_locations WHERE state_id = NEW.state_id AND element_id = (SELECT id FROM puzzle_elements WHERE name = 'Goat') INTO @goat_loc;
    -- SELECT location_id FROM state_element_locations WHERE state_id = NEW.state_id AND element_id = (SELECT id FROM puzzle_elements WHERE name = 'Cabbage') INTO @cabbage_loc;
    -- SELECT location_id FROM state_element_locations WHERE state_id = NEW.state_id AND element_id = (SELECT id FROM puzzle_elements WHERE name = 'Human') INTO @human_loc;
    -- SELECT location_id FROM state_element_locations WHERE state_id = NEW.state_id AND element_id = (SELECT id FROM puzzle_elements WHERE name = 'Wolf') INTO @wolf_loc;

    -- Constraint: Goat cannot be left alone with Cabbage
    -- If Goat and Cabbage are on the same bank AND Human is NOT on that bank
    SELECT RAISE(ABORT, 'Goat and Cabbage left alone!')
    FROM (
        SELECT
            (SELECT location_id FROM state_element_locations WHERE state_id = NEW.state_id AND element_id = (SELECT id FROM puzzle_elements WHERE name = 'Goat')) AS goat_loc,
            (SELECT location_id FROM state_element_locations WHERE state_id = NEW.state_id AND element_id = (SELECT id FROM puzzle_elements WHERE name = 'Cabbage')) AS cabbage_loc,
            (SELECT location_id FROM state_element_locations WHERE state_id = NEW.state_id AND element_id = (SELECT id FROM puzzle_elements WHERE name = 'Human')) AS human_loc,
            (SELECT location_id FROM state_element_locations WHERE state_id = NEW.state_id AND element_id = (SELECT id FROM puzzle_elements WHERE name = 'Wolf')) AS wolf_loc
    ) AS current_state
    WHERE current_state.goat_loc = current_state.cabbage_loc
      AND current_state.human_loc != current_state.goat_loc;

    -- Constraint: Wolf cannot be left alone with Cabbage
    -- If Wolf and Cabbage are on the same bank AND Human is NOT on that bank
    SELECT RAISE(ABORT, 'Wolf and Cabbage left alone!')
    FROM (
        SELECT
            (SELECT location_id FROM state_element_locations WHERE state_id = NEW.state_id AND element_id = (SELECT id FROM puzzle_elements WHERE name = 'Goat')) AS goat_loc,
            (SELECT location_id FROM state_element_locations WHERE state_id = NEW.state_id AND element_id = (SELECT id FROM puzzle_elements WHERE name = 'Cabbage')) AS cabbage_loc,
            (SELECT location_id FROM state_element_locations WHERE state_id = NEW.state_id AND element_id = (SELECT id FROM puzzle_elements WHERE name = 'Human')) AS human_loc,
            (SELECT location_id FROM state_element_locations WHERE state_id = NEW.state_id AND element_id = (SELECT id FROM puzzle_elements WHERE name = 'Wolf')) AS wolf_loc
    ) AS current_state
    WHERE current_state.wolf_loc = current_state.cabbage_loc
      AND current_state.human_loc != current_state.wolf_loc;

    -- Additional constraints could be added here for other puzzles,
    -- e.g., "Human can only carry one item at a time" would be checked
    -- during the transition generation logic in the external solver,
    -- not necessarily as a state validity constraint.
END;
```

## Benefits of this Rationalized Approach

1.  **True Generality (X-Dimensionality):** The `puzzle_states` and `state_element_locations` tables can now represent any puzzle with any number of elements, simply by adding new elements to the `puzzle_elements` table. No schema changes are needed for `puzzle_states` itself.
2.  **Enhanced Flexibility:** New puzzles or variations (e.g., adding a "dog" element) only require updating `puzzle_elements` and potentially modifying the trigger logic to include new safety rules.
3.  **Declarative Constraint Definition:** The safety rules are explicitly defined within the database, making them transparent, auditable, and consistently enforced.
4.  **Robustness by Design:** The database guarantees that any state recorded in `puzzle_states` is inherently valid according to the defined rules. This shifts the burden of validation from the external solver to the database itself.
5.  **Improved Transferability:** This architectural pattern can be directly applied to a wide range of state-space search problems, from other river crossing variations to more complex logistics or game-state validation scenarios. The "law" becomes a reusable template.

This refined architecture embodies the principle of "invent the law and then live by it fully, as it is YOUR law," providing a powerful and adaptable framework for solving a class of logic puzzles.
