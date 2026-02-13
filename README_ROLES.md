# GeneRisk AI - Role-Based Access System

## Overview
The GeneRisk AI platform now features a comprehensive role-based access control system with interactive dashboards for different user types.

## User Roles

### 1. Patient/User (`user`)
**Access Level:** Basic
- Upload gene expression data
- View personal prediction results
- Access prediction history
- Contact support

**Dashboard Features:**
- Personal profile information
- Quick upload functionality
- Results history access
- Help and support options

### 2. Doctor (`doctor`)
**Access Level:** Medical Professional
- All user capabilities
- View patient prediction results
- Add clinical notes to patient files
- Access medical analytics dashboard
- Generate patient reports

**Dashboard Features:**
- Patient management interface
- Clinical notes system
- Medical analytics and statistics
- High-risk patient alerts
- Professional reporting tools

### 3. Researcher (`researcher`)
**Access Level:** Research Professional
- All user capabilities
- Advanced dataset analysis
- Biomarker research tools
- Model performance evaluation
- Cross-cancer analysis
- Research data export

**Dashboard Features:**
- Dataset upload and analysis
- Biomarker comparison tools
- Model performance metrics
- Cross-cancer gene analysis
- Research statistics and trends
- Publication management

### 4. Administrator (`admin`)
**Access Level:** Full System Access
- All system capabilities
- User management
- System configuration
- Audit logs and monitoring
- System health monitoring

**Dashboard Features:**
- User account management
- System-wide analytics
- Configuration settings
- Audit trail access
- System status monitoring

## Getting Started

### 1. Setup Demo Users
```bash
cd comb_disease_predictor
python demo_setup.py
```

### 2. Run the Application
```bash
python backend/app.py
```

### 3. Access the System
Navigate to `http://localhost:5000` and login with demo credentials:

- **Patient:** patient@demo.com / demo123
- **Doctor:** doctor@demo.com / demo123
- **Researcher:** researcher@demo.com / demo123
- **Admin:** admin@demo.com / demo123

## Key Features

### Role-Based Navigation
- Dynamic navigation menus based on user role
- Role-specific dropdown menus for advanced features
- User profile display with role identification

### Access Control
- Route-level access restrictions using decorators
- Automatic redirection for unauthorized access
- Error handling for forbidden resources

### Interactive Dashboards
- Role-specific dashboard layouts
- Quick action buttons and tools
- Real-time statistics and monitoring
- Professional-grade interface design

### Security Features
- Password hashing with Werkzeug
- Session-based authentication with Flask-Login
- Role-based authorization decorators
- Secure route protection

## File Structure
```
backend/
├── decorators.py          # Role-based access decorators
├── templates/
│   ├── login.html         # Enhanced login with registration link
│   ├── register.html      # Role selection registration
│   ├── user_dashboard.html    # Patient dashboard
│   ├── doctor_dashboard.html  # Medical professional dashboard
│   ├── researcher_dashboard.html # Research dashboard
│   ├── admin_dashboard.html   # Administrator dashboard
│   ├── doctor_notes.html      # Clinical notes management
│   ├── doctor_analytics.html  # Medical analytics
│   ├── research_biomarkers.html # Biomarker research
│   ├── research_models.html    # Model performance
│   ├── research_cross_analysis.html # Cross-cancer analysis
│   ├── error.html         # Access denied page
│   └── index.html         # Enhanced upload page
└── routes/
    └── dashboard.py       # Enhanced with role-specific routes
```

## Usage Examples

### For Patients
1. Register with "Patient/User" role
2. Upload gene expression data
3. View personalized risk reports
4. Access prediction history

### For Doctors
1. Register with "Doctor" role
2. Access patient management tools
3. Add clinical notes to patient files
4. View medical analytics and alerts
5. Generate professional reports

### For Researchers
1. Register with "Researcher" role
2. Upload research datasets
3. Analyze biomarkers across cancer types
4. Evaluate model performance
5. Conduct cross-cancer analysis
6. Export research data

### For Administrators
1. Use admin credentials
2. Manage user accounts and permissions
3. Monitor system health and performance
4. Access audit logs and system analytics
5. Configure system settings

## Technical Implementation

### Role-Based Decorators
```python
@role_required('doctor', 'researcher')
def restricted_route():
    # Only doctors and researchers can access
    pass
```

### Dynamic Navigation
The navigation bar automatically adjusts based on user role, showing relevant tools and hiding unauthorized sections.

### Error Handling
Proper error pages for unauthorized access (401) and forbidden resources (403) with user-friendly messages and navigation options.