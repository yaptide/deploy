# Sequence diagrams

## Overview of run simulation sequence

This is scenario used when direct job submission is used and simulation job is executed in Celery worker.

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant FrontendApp as JavaScript App in Browser
    box Backend
    participant BackendApp as Flask
    participant Database as Database
    participant CeleryQueue as Celery Queue
    end

    User->>FrontendApp: Run simulation
    activate FrontendApp
    FrontendApp->>BackendApp: POST /jobs/direct
    activate BackendApp
    BackendApp->>+BackendApp: Create Simulation object internally
    BackendApp->>CeleryQueue: Submit job
    activate CeleryQueue
    CeleryQueue-->>BackendApp: Return Job ID
    deactivate CeleryQueue
    BackendApp->>+BackendApp: Update Simulation object with Job ID
    BackendApp->>Database: Commit Simulation object to Database
    activate Database
    Database-->>BackendApp: Acknowledge Commit
    deactivate BackendApp
    deactivate Database
    BackendApp-->>FrontendApp: POST /jobs/direct response (Simulation ID)
    FrontendApp->>User: Add new simulation card
    loop Progress check every 2 seconds
        FrontendApp->>BackendApp: GET /jobs?job_id={job_id}
        BackendApp->>Database: Query Simulation status
        activate Database
        Database-->>BackendApp: Return Simulation status
        deactivate Database
        BackendApp-->>FrontendApp: Return Simulation status
        opt status changed
            FrontendApp->>User: Update progress 
        end
        opt status is completed
            FrontendApp->>BackendApp: GET /results?job_id={job_id}
            activate BackendApp
            BackendApp->>Database: Query Simulation results
            activate Database
            Database-->>BackendApp: Return Simulation results
            deactivate Database
            BackendApp-->>FrontendApp: Return Simulation results
            deactivate BackendApp
            FrontendApp->>User: Display results
        end
    end
    deactivate FrontendApp
```

### Job submission in more details

```mermaid
sequenceDiagram
    autonumber
    participant Client as REST Client
    participant BackendApp as Flask
    participant Database as Database
    participant CeleryQueue as Celery Queue
    participant CeleryBroker as Celery Broker (Redis)

    activate Client
    Client->>BackendApp: POST /jobs/direct
    activate BackendApp
    BackendApp->>+BackendApp: Create Simulation object internally
    BackendApp->>CeleryQueue: Submit job
    activate CeleryQueue
    CeleryQueue->>CeleryBroker: Queue simulation tasks
    CeleryQueue->>CeleryBroker: Queue merge task
    CeleryQueue-->>BackendApp: Return merge task (chord) id
    deactivate CeleryQueue
    BackendApp->>+BackendApp: Update Simulation object with Job ID
    BackendApp->>Database: Commit Simulation object to Database
    activate Database
    Database-->>BackendApp: Acknowledge Commit
    deactivate BackendApp
    deactivate Database
    BackendApp-->>Client: POST /jobs/direct response (Simulation ID)
    deactivate Client
```

Single task execution:

```mermaid
sequenceDiagram
    # simulation execution
    autonumber
    participant Client as REST Client
    participant BackendApp as Flask
    participant Database as Database
    participant CeleryQueue as Celery Queue
    participant CeleryBroker as Celery Broker (Redis)
    participant CeleryBackend as Celery Backend (Redis)
    participant CeleryWorker as Celery Worker
    participant SimulationProcess as Simulation process
    participant LogsWatcher as Simulation monitor
    participant SimulationLogs as Simulation logfile
    participant SimulationOutput as Simulation output file

    activate CeleryWorker
    CeleryBroker->>CeleryWorker: Fetch simulation task

    CeleryWorker->>BackendApp: POST /tasks
    activate BackendApp
    BackendApp->>Database: Commit update of task object
    activate Database
    Database-->>BackendApp: Acknowledge Commit
    deactivate Database
    BackendApp-->>CeleryWorker: POST /tasks response
    deactivate BackendApp

    CeleryWorker->>LogsWatcher: Starts monitoring process
    activate LogsWatcher
    CeleryWorker->>SimulationProcess: Starts simulation process
    activate SimulationProcess

    par logfile production
        loop every 1000 primary particles
            SimulationProcess->>SimulationLogs: Appends lines with status
        end
    and logfile monitoring
        loop watch logfile for new lines
            LogsWatcher->>SimulationLogs: Reads line with progress

            LogsWatcher->>BackendApp: POST /tasks (not often than every 2 seconds)
            activate BackendApp
            BackendApp->>Database: Commit update of task object
            activate Database
            Database-->>BackendApp: Acknowledge Commit
            deactivate Database
            BackendApp-->>LogsWatcher: POST /tasks response
            deactivate BackendApp
        end
    end

    SimulationProcess->>SimulationOutput: Saves output file
    deactivate SimulationProcess
    deactivate LogsWatcher

    CeleryWorker->>SimulationOutput: Reads output into JSON

    CeleryWorker->>BackendApp: POST /tasks
    activate BackendApp
    BackendApp->>Database: Commit update of task object
    activate Database
    Database-->>BackendApp: Acknowledge Commit
    deactivate Database
    BackendApp-->>CeleryWorker: POST /tasks response
    deactivate BackendApp

    CeleryWorker->>CeleryBackend: Save task results

    deactivate CeleryWorker
```