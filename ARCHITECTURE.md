# AI-Powered Paraguay Newcomer App - System Architecture

## 🎯 Project Overview
**Goal**: Help newcomers (mainly Brazilians) get AI-assisted guidance on Paraguayan bureaucracy, documents, and local adaptation via a chat-based interface with localized information.

**Tech Stack**: Django Backend + Next.js Frontend + Flutter Mobile + PostgreSQL with pgvector

---

## 🏗️ System Architecture

### Backend (Django) - Core AI & Data Layer
**Location**: `/cheguia-backend/`
**Purpose**: Handle AI processing, data management, and business logic

#### Apps Structure:
```
cheguia-backend/
├── ai/           # AI processing, embeddings, RAG
├── chat/         # Chat history, sessions, messages
├── documents/    # Document templates, knowledge base
├── users/        # User management, authentication
└── api/          # REST API endpoints
```

#### Core Responsibilities:
- **AI Processing**: LangChain + OpenAI integration
- **RAG System**: Document retrieval and context building
- **Chat Management**: Message history, sessions, user context
- **Document Templates**: Dynamic document generation
- **User Management**: Authentication, progress tracking
- **Knowledge Base**: Document storage and vector embeddings

### Frontend (Next.js) - Web Interface
**Location**: `/cheguia-frontend/` (to be created)
**Purpose**: Web-based user interface

#### Features:
- Chat interface with message bubbles
- Document template generator
- Progress tracking dashboard
- Language switcher (Spanish/Portuguese)
- User authentication UI
- Desktop-optimized design

### Mobile (Flutter) - Mobile Interface
**Location**: `/cheguia-mobile/` (to be created)
**Purpose**: Native mobile experience

#### Features:
- Native chat interface with smooth animations
- Offline document storage and sync
- Push notifications for document reminders
- Camera integration for document scanning
- GPS integration for location-based services
- Native performance and UX

### Database (PostgreSQL + pgvector)
**Purpose**: Store all application data including vector embeddings

#### Key Tables:
- **Users**: Authentication, preferences, subscription status
- **Chats**: Chat sessions and message history
- **Documents**: Knowledge base documents and metadata
- **Document_embeddings**: Vector embeddings for RAG
- **Templates**: Document templates for generation
- **User_progress**: Checklist progress and completion

---

## 🔧 Technical Implementation

### Django Backend Configuration

#### Settings Updates Needed:
```python
# settings.py additions
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'ai',
    'chat', 
    'documents',
    'users',
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'paraguay_guide',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# CORS for Next.js frontend and Flutter mobile
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Next.js dev
    "https://yourdomain.com", # Production web
    # Flutter mobile apps use different origins
]

CORS_ALLOW_ALL_ORIGINS = True  # For development only
```

#### API Endpoints Structure:
```
/api/
├── auth/           # Authentication endpoints
├── chat/           # Chat functionality
├── documents/      # Document management
├── templates/      # Template generation
├── users/          # User management
├── ai/             # AI processing endpoints
└── mobile/         # Mobile-specific endpoints (offline sync, etc.)
```

### Flutter Mobile App Structure

#### Project Organization:
```
cheguia-mobile/
├── lib/
│   ├── main.dart
│   ├── app/
│   │   ├── app.dart
│   │   └── routes.dart
│   ├── core/
│   │   ├── constants/
│   │   ├── errors/
│   │   ├── network/
│   │   └── utils/
│   ├── features/
│   │   ├── auth/
│   │   ├── chat/
│   │   ├── documents/
│   │   ├── profile/
│   │   └── settings/
│   ├── shared/
│   │   ├── widgets/
│   │   ├── services/
│   │   └── models/
│   └── l10n/       # Localization files
├── android/
├── ios/
└── pubspec.yaml
```

#### Key Flutter Packages:
```yaml
dependencies:
  flutter:
    sdk: flutter
  
  # State Management
  bloc: ^8.1.0
  flutter_bloc: ^8.1.0
  
  # Networking
  dio: ^5.3.0
  retrofit: ^4.0.0
  
  # Local Storage & Sync
  hive: ^2.2.3
  hive_flutter: ^1.1.0
  
  # UI & Animations
  flutter_animate: ^4.2.0
  shimmer: ^3.0.0
  
  # Camera & Documents
  camera: ^0.10.5
  file_picker: ^6.1.0
  pdf: ^3.10.0
  
  # Push Notifications
  firebase_messaging: ^14.6.0
  
  # Location
  geolocator: ^10.1.0
  
  # Internationalization
  flutter_localizations:
    sdk: flutter
  intl: ^0.18.0
```

### PostgreSQL + pgvector Setup

#### Required Extensions:
```sql
-- Enable vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

#### Key Database Schema:
```sql
-- Documents table with vector embeddings
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    source_url VARCHAR(1000),
    document_type VARCHAR(100),
    language VARCHAR(10),
    created_at TIMESTAMP DEFAULT NOW(),
    embedding vector(1536) -- OpenAI embedding dimension
);

-- Chat sessions
CREATE TABLE chat_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    title VARCHAR(200),
    platform VARCHAR(20), -- 'web', 'mobile'
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Messages
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES chat_sessions(id),
    role VARCHAR(20) NOT NULL, -- 'user' or 'assistant'
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Mobile-specific: Offline sync tracking
CREATE TABLE sync_queue (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(20), -- 'create', 'update', 'delete'
    table_name VARCHAR(50),
    record_id UUID,
    data JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    synced_at TIMESTAMP
);
```

---

## 🚀 Development Phases

### Phase 1: Foundation (Week 1)
**Backend Tasks:**
- [ ] Set up PostgreSQL with pgvector
- [ ] Configure Django settings for new apps
- [ ] Create basic models for users, chats, documents
- [ ] Set up LangChain + OpenAI integration
- [ ] Create basic chat API endpoint

**Web Frontend Tasks:**
- [ ] Create Next.js project with TypeScript
- [ ] Set up Tailwind CSS and basic UI components
- [ ] Create chat interface mockup
- [ ] Connect to Django API

**Mobile Tasks:**
- [ ] Create Flutter project structure
- [ ] Set up BLoC state management
- [ ] Create basic chat UI with animations
- [ ] Implement API client with Dio

### Phase 2: RAG Integration (Week 2)
**Backend Tasks:**
- [ ] Implement document embedding system
- [ ] Create RAG pipeline with vector similarity search
- [ ] Add document ingestion from Paraguay sources
- [ ] Implement source citation in responses
- [ ] Add language detection and localization

**Web Frontend Tasks:**
- [ ] Enhance chat UI with message bubbles
- [ ] Add source citations display
- [ ] Implement language switcher
- [ ] Add loading states and error handling

**Mobile Tasks:**
- [ ] Implement offline-first chat storage with Hive
- [ ] Add pull-to-refresh and infinite scroll
- [ ] Create native language switcher
- [ ] Add haptic feedback for interactions

### Phase 3: Document Features (Week 3)
**Backend Tasks:**
- [ ] Create document template system
- [ ] Implement dynamic template filling
- [ ] Add checklist generation based on visa types
- [ ] Create translation service (Portuguese ↔ Spanish)

**Web Frontend Tasks:**
- [ ] Build document template interface
- [ ] Add checklist progress tracking
- [ ] Implement template download functionality
- [ ] Create progress dashboard

**Mobile Tasks:**
- [ ] Add camera integration for document scanning
- [ ] Implement offline document storage
- [ ] Create native checklist with progress tracking
- [ ] Add share functionality for templates

### Phase 4: Polish & Launch (Week 4)
**Backend Tasks:**
- [ ] Add user authentication (Supabase or Django Auth)
- [ ] Implement subscription/premium features
- [ ] Add chat history and user progress storage
- [ ] Set up production database and environment
- [ ] Add push notification service

**Web Frontend Tasks:**
- [ ] Add authentication UI
- [ ] Implement premium feature gates
- [ ] Add feedback system (thumbs up/down)
- [ ] Desktop optimization and testing

**Mobile Tasks:**
- [ ] Add Firebase push notifications
- [ ] Implement biometric authentication
- [ ] Add location-based services
- [ ] Create app store listings and assets
- [ ] Add deep linking for document sharing

---

## 🔐 Environment Variables

### Django Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/paraguay_guide

# OpenAI
OPENAI_API_KEY=your_openai_key

# Django
SECRET_KEY=your_django_secret_key
DEBUG=True

# CORS
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Supabase (if using for auth)
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key

# Firebase (for mobile push notifications)
FIREBASE_SERVER_KEY=your_firebase_server_key
```

### Next.js Frontend (.env.local)
```bash
# API
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws

# Supabase
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key

# Stripe (for payments)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=your_stripe_key
```

### Flutter Mobile (config files)
```dart
// lib/core/constants/api_constants.dart
class ApiConstants {
  static const String baseUrl = 'https://yourdomain.com/api';
  static const String wsUrl = 'wss://yourdomain.com/ws';
}

// lib/core/constants/app_constants.dart
class AppConstants {
  static const String appName = 'Paraguay Guide';
  static const String version = '1.0.0';
}
```

---

## 📁 Project Structure

```
paraguay-project/
├── cheguia-backend/          # Django backend
│   ├── ai/                   # AI processing
│   ├── chat/                 # Chat functionality  
│   ├── documents/            # Document management
│   ├── users/                # User management
│   ├── api/                  # REST API
│   ├── cheguia/              # Django settings
│   ├── requirements.txt      # Python dependencies
│   └── manage.py
├── cheguia-frontend/         # Next.js web frontend (to create)
│   ├── app/                  # App Router
│   ├── components/           # React components
│   ├── lib/                  # Utilities
│   ├── public/               # Static assets
│   └── package.json
├── cheguia-mobile/           # Flutter mobile app (to create)
│   ├── lib/                  # Dart source code
│   ├── android/              # Android configuration
│   ├── ios/                  # iOS configuration
│   ├── assets/               # Images, fonts, etc.
│   └── pubspec.yaml
├── data/                     # Knowledge base documents
│   ├── migraciones/          # Immigration docs
│   ├── set/                  # Tax authority docs
│   └── ande/                 # Electric company docs
└── docs/                     # Documentation
    └── ARCHITECTURE.md       # This file
```

---

## 🔄 Data Flow

### Web Flow:
1. **User Input** → Next.js Frontend
2. **API Request** → Django Backend
3. **Query Processing** → AI App (LangChain)
4. **Document Retrieval** → RAG System (pgvector)
5. **Context Building** → Relevant documents + embeddings
6. **AI Response** → OpenAI with context
7. **Response** → Django → Next.js → User

### Mobile Flow:
1. **User Input** → Flutter App
2. **Local Storage** → Hive (offline-first)
3. **API Sync** → Django Backend (when online)
4. **Background Sync** → Sync queue processing
5. **Push Notifications** → Firebase → Flutter
6. **Offline Mode** → Local data with sync indicators

---

## 📱 Mobile-Specific Features

### Offline-First Architecture:
- **Local Storage**: Hive for chat history, documents, progress
- **Sync Queue**: Track changes when offline, sync when online
- **Background Sync**: Automatic sync in background
- **Conflict Resolution**: Last-write-wins with user notification

### Native Features:
- **Camera Integration**: Scan documents directly
- **GPS**: Location-based services (find nearest offices)
- **Push Notifications**: Document reminders, chat updates
- **Biometric Auth**: Fingerprint/Face ID login
- **Share**: Native sharing of templates and documents

### Performance Optimizations:
- **Lazy Loading**: Load chat history progressively
- **Image Caching**: Cache document images locally
- **Background Processing**: Process embeddings in background
- **Memory Management**: Efficient image and data handling

---

## 🎯 Success Metrics

- **Response Accuracy**: AI provides correct, source-cited information
- **User Engagement**: Users complete document checklists
- **Performance**: <2s response time for chat queries
- **Mobile Performance**: <1s app startup, smooth animations
- **Offline Capability**: Full functionality without internet
- **Scalability**: Handle 100+ concurrent users
- **Localization**: Seamless Spanish/Portuguese experience

---

## 🚀 Deployment Strategy

### Development
- Django: `python manage.py runserver`
- Next.js: `npm run dev`
- Flutter: `flutter run`
- PostgreSQL: Local instance with pgvector

### Production
- Django: AWS EC2 or Railway
- Next.js: Vercel deployment
- Flutter: Google Play Store + Apple App Store
- PostgreSQL: AWS RDS with pgvector extension
- Static Files: AWS S3
- Push Notifications: Firebase
- Domain: Custom domain with SSL

### Mobile Deployment:
- **Android**: Google Play Store (direct upload)
- **iOS**: Apple App Store (TestFlight → Production)
- **CI/CD**: GitHub Actions for automated builds
- **Code Signing**: Automated certificate management

---

## 🔄 Cross-Platform Sync Strategy

### Data Synchronization:
1. **User Actions** → Local storage (immediate)
2. **Background Sync** → Server (when online)
3. **Conflict Resolution** → Server timestamp wins
4. **Push Updates** → Firebase → All devices

### Shared Features:
- **Chat History**: Sync across all platforms
- **Document Progress**: Unified progress tracking
- **User Preferences**: Language, notifications, etc.
- **Subscription Status**: Consistent across platforms

---

*This architecture document should be updated as the project evolves and requirements change.*