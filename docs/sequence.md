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