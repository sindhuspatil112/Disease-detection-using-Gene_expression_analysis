# GeneRisk AI - System Architecture Flowchart

## High-Level System Architecture

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[Web Interface<br/>HTML Templates]
        CSS[Static Assets<br/>CSS/Images]
    end
    
    subgraph "Application Layer"
        Flask[Flask Web Server<br/>app.py]
        Auth[Authentication<br/>Flask-Login]
        Routes[Route Handlers<br/>Blueprints]
    end
    
    subgraph "Business Logic Layer"
        Pred[Prediction Engine<br/>run_predictions.py]
        Preproc[Data Preprocessing<br/>preprocess.py]
        Models[ML Models<br/>PKL Files]
    end
    
    subgraph "Data Layer"
        DB[(SQLite Database<br/>User & Prediction Data)]
        Files[Gene Expression Files<br/>CSV/TXT]
    end
    
    UI --> Flask
    CSS --> Flask
    Flask --> Auth
    Flask --> Routes
    Routes --> Pred
    Routes --> DB
    Pred --> Preproc
    Pred --> Models
    Preproc --> Files
```

## Detailed Component Architecture

```mermaid
graph LR
    subgraph "User Roles & Access"
        Patient[Patient/User]
        Doctor[Doctor]
        Researcher[Researcher]
        Admin[Administrator]
    end
    
    subgraph "Authentication & Authorization"
        Login[Login System]
        RoleCheck[Role-Based Access Control]
        Session[Session Management]
    end
    
    subgraph "Core Application Routes"
        Dashboard[Dashboard Routes]
        Upload[File Upload Routes]
        History[Prediction History]
        Analytics[Analytics Routes]
    end
    
    subgraph "ML Pipeline"
        FileProc[File Processing]
        GeneMap[Gene Mapping]
        Normalize[Data Normalization]
        Predict[Model Prediction]
    end
    
    subgraph "Disease Models"
        Breast[Breast Cancer Model]
        Lung[Lung Cancer Model]
        Ovarian[Ovarian Cancer Model]
        Cross[Cross-Cancer Models]
    end
    
    Patient --> Login
    Doctor --> Login
    Researcher --> Login
    Admin --> Login
    
    Login --> RoleCheck
    RoleCheck --> Session
    Session --> Dashboard
    Session --> Upload
    Session --> History
    Session --> Analytics
    
    Upload --> FileProc
    FileProc --> GeneMap
    GeneMap --> Normalize
    Normalize --> Predict
    
    Predict --> Breast
    Predict --> Lung
    Predict --> Ovarian
    Predict --> Cross
```

## Data Flow Architecture

```mermaid
sequenceDiagram
    participant User
    participant WebApp
    participant Auth
    participant Routes
    participant Preprocessor
    participant MLEngine
    participant Database
    
    User->>WebApp: Upload Gene Expression File
    WebApp->>Auth: Verify User Session
    Auth-->>WebApp: Session Valid
    WebApp->>Routes: Route to Upload Handler
    Routes->>Preprocessor: Process Raw Data
    
    Note over Preprocessor: Gene mapping, normalization, validation
    
    Preprocessor-->>Routes: Processed DataFrame
    Routes->>MLEngine: Run Predictions
    
    Note over MLEngine: Load models, feature alignment, prediction
    
    MLEngine-->>Routes: Prediction Results
    Routes->>Database: Store Results
    Database-->>Routes: Confirmation
    Routes-->>WebApp: Render Results
    WebApp-->>User: Display Predictions
```

## Database Schema Architecture

```mermaid
erDiagram
    User {
        int id PK
        string name
        string email UK
        string password
        string role
    }
    
    Prediction {
        int id PK
        string filename
        text results_json
        text shared_json
        int user_id FK
        datetime timestamp
    }
    
    DoctorNote {
        int id PK
        int prediction_id
        int doctor_id
        text notes
        datetime timestamp
    }
    
    SharedReport {
        int id PK
        int prediction_id FK
        int from_user_id FK
        int to_user_id FK
        text message
        string status
        datetime timestamp
    }
    
    Consultation {
        int id PK
        int patient_id FK
        int doctor_id FK
        int prediction_id FK
        text medical_advice
        string status
        datetime timestamp
    }
    
    User ||--o{ Prediction : creates
    User ||--o{ SharedReport : sends
    User ||--o{ SharedReport : receives
    User ||--o{ Consultation : participates
    Prediction ||--o{ SharedReport : references
    Prediction ||--o{ Consultation : discusses
```

## ML Model Architecture

```mermaid
graph TB
    subgraph "Input Processing"
        RawFile[Raw Gene Expression File]
        Validate[File Validation]
        Parse[Data Parsing]
        Clean[Data Cleaning]
    end
    
    subgraph "Feature Engineering"
        GeneMap[Gene ID Mapping]
        Normalize[Expression Normalization]
        Select[Feature Selection]
        Align[Model Alignment]
    end
    
    subgraph "Prediction Models"
        BreastModel[Breast Cancer<br/>Balanced Model]
        LungModel[Lung Cancer<br/>Balanced Model]
        OvarianModel[Ovarian Cancer<br/>Balanced Model]
        CrossModel[Cross-Cancer<br/>Union Model]
    end
    
    subgraph "Output Processing"
        Ensemble[Risk Score Calculation]
        Confidence[Confidence Intervals]
        Report[Result Formatting]
        Store[Database Storage]
    end
    
    RawFile --> Validate
    Validate --> Parse
    Parse --> Clean
    Clean --> GeneMap
    GeneMap --> Normalize
    Normalize --> Select
    Select --> Align
    
    Align --> BreastModel
    Align --> LungModel
    Align --> OvarianModel
    Align --> CrossModel
    
    BreastModel --> Ensemble
    LungModel --> Ensemble
    OvarianModel --> Ensemble
    CrossModel --> Ensemble
    
    Ensemble --> Confidence
    Confidence --> Report
    Report --> Store
```

## Security & Access Control Architecture

```mermaid
graph TB
    subgraph "Security Layers"
        Input[Input Validation]
        Auth[Authentication]
        Authz[Authorization]
        Session[Session Security]
    end
    
    subgraph "Role-Based Access"
        UserRole[User Role<br/>- Upload files<br/>- View own results]
        DoctorRole[Doctor Role<br/>- Patient consultation<br/>- Medical notes<br/>- Analytics]
        ResearcherRole[Researcher Role<br/>- Biomarker analysis<br/>- Cross-cancer studies<br/>- Model metrics]
        AdminRole[Admin Role<br/>- User management<br/>- System analytics<br/>- Full access]
    end
    
    subgraph "Data Protection"
        Encrypt[Password Hashing]
        Sanitize[Input Sanitization]
        Validate[File Validation]
        Audit[Access Logging]
    end
    
    Input --> Auth
    Auth --> Authz
    Authz --> Session
    
    Session --> UserRole
    Session --> DoctorRole
    Session --> ResearcherRole
    Session --> AdminRole
    
    Auth --> Encrypt
    Input --> Sanitize
    Input --> Validate
    Session --> Audit
```

## Deployment Architecture

```mermaid
graph TB
    subgraph "Development Environment"
        DevServer[Flask Dev Server<br/>localhost:5000]
        DevDB[SQLite Database<br/>data.db]
        DevFiles[Local File Storage]
    end
    
    subgraph "Production Environment"
        WebServer[Web Server<br/>Nginx/Apache]
        AppServer[WSGI Server<br/>Gunicorn/uWSGI]
        ProdDB[Production Database<br/>PostgreSQL/MySQL]
        FileStorage[File Storage<br/>AWS S3/Local]
    end
    
    subgraph "Model Storage"
        ModelFiles[Trained Models<br/>.pkl files]
        GeneData[Gene Mappings<br/>.json files]
        Biomarkers[Biomarker Data<br/>.csv files]
    end
    
    DevServer --> AppServer
    DevDB --> ProdDB
    DevFiles --> FileStorage
    
    AppServer --> ModelFiles
    AppServer --> GeneData
    AppServer --> Biomarkers
```

## Key System Components

### 1. **Web Application Layer**
- Flask-based web server with role-based authentication
- Responsive HTML templates for different user roles
- RESTful API endpoints for file uploads and predictions

### 2. **Machine Learning Pipeline**
- Multi-cancer prediction models (Breast, Lung, Ovarian)
- Gene expression data preprocessing and normalization
- Cross-cancer analysis capabilities

### 3. **Data Management**
- SQLite database for user and prediction storage
- File handling for gene expression datasets
- Secure data validation and sanitization

### 4. **User Management**
- Role-based access control (Patient, Doctor, Researcher, Admin)
- Secure authentication with password hashing
- Session management and authorization

### 5. **Analytics & Reporting**
- Prediction history tracking
- Performance metrics and model evaluation
- Collaborative features for medical consultation

This architecture supports scalable, secure, and maintainable cancer risk prediction with clear separation of concerns and role-based functionality.