flowchart TB
    subgraph Initialization
    initialization("Initialization of matrix 5 by 5 and variables")
    initialization --> count
    initialization --> x
    initialization --> y
    initialization --> step
    initialization --> direction
    initialization --> matrix
    count("Count")
    x("X")
    y("Y")
    step("Step")
    direction("Direction")
    end

    subgraph Move
    x_plus("x += 1")
    y_plus("y += 1")
    x_minus("x -= 1")
    y_minus("y -= 1")

    decision_right{direction mod 4 = 0?}
    decision_down{direction mod 4 = 1?}
    decision_left{direction mod 4 = 2?}

    direction --> decision_right
    direction --> decision_down
    direction --> decision_left

    decision_right -- Yes --> x_plus
    decision_right -- No --> decision_down
    decision_down -- Yes --> y_plus
    decision_down -- No --> decision_left
    decision_left -- Yes --> x_minus
    decision_left -- No --> y_minus
    
    end
    
    x_plus --> direction_update("Update direction")
    y_plus --> direction_update
    x_minus --> direction_update
    y_minus --> direction_update

    subgraph Main Loop
    count --> assign_red("Assign the 🟥 red element to matrix")
    direction_update --> step_increment["Increment step if moving right or left"]
    assign_red --> matrix["Move the 🟥 red element to matrix"]
    step_increment --> print_result["Print intermediate result"]
    
    direction_update -.->|Update direction| step_increment
    step_increment -->|Increment step| step

    end
    
    count --> count
    x_plus --> x
    y_plus --> y
    x_minus --> x
    y_minus --> y
    assign_red --> matrix
    direction --> decision_right
    direction --> decision_down
    direction --> decision_left
    initialization -.-> count
    matrix("Matrix")

    x -.->|Move to the left| x_minus
    y -.->|Move up| y_minus
    x -.->|Move to the right| x_plus
    y -.->|Move down| y_plus

    direction -.-> decision_right
    direction -.-> decision_down
    direction -.-> decision_left

