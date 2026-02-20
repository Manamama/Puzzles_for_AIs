sequenceDiagram
    participant matrix as Matrix
    participant count as Count
    participant x as X
    participant y as Y
    participant step as Step
    participant direction as Direction
    participant n as N

    Note over matrix, count: Initialization 
    Note over x, y: Initialization
    Note over step, direction: Initialization
    Note over n: Initialization

    Note over matrix: Create an empty matrix with all white squares

    loop Until Termination
        Note over count, matrix: Start Spiral Iteration

        Note over count, matrix: Assign red square to current position in matrix
        count-->>count: Increment count

        Note over direction: Move in the current direction

        direction->>x: If moving right
        direction->>y: If moving down
        direction-->>x: If moving left
        direction-->>y: If moving up

        Note over matrix: Print intermediate matrix
        matrix-->>matrix: Print matrix

        Note over direction: Update direction

        direction-->>+step: If moving right or left, increment step

        Note over count: Check termination condition
        count-->n: If count reaches n*n

    end

