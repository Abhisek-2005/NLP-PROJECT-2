from fastapi import APIRouter
import datetime
from backend.app.config import settings
from backend.app.services.matcher import matcher_pipeline

router = APIRouter(tags=["System & Samples"])

@router.get("/health", summary="Health Check")
async def health_check():
    """System health check and NLP model operational status."""
    return {
        "status": "online",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "nlp_model": matcher_pipeline.similarity_service.model_name,
        "is_fallback": matcher_pipeline.similarity_service.is_fallback,
        "fallback_reason": matcher_pipeline.similarity_service.fallback_reason,
        "weights": {
            "semantic": settings.SEMANTIC_WEIGHT,
            "skill": settings.SKILL_WEIGHT,
            "keyword": settings.KEYWORD_WEIGHT
        }
    }

@router.get("/samples", summary="Get Pre-configured Sample Resumes & Job Descriptions")
async def get_samples():
    """Returns realistic resumes and job descriptions for rapid testing and demonstrations."""
    samples = [
        {
            "id": "ml-nlp-engineer",
            "role": "Machine Learning / NLP Engineer",
            "job_title": "Senior NLP & Machine Learning Engineer",
            "job_description": """Job Title: Senior NLP & Machine Learning Engineer
Location: Remote / Hybrid

About The Role:
We are seeking an experienced Machine Learning Engineer with deep specialization in Natural Language Processing (NLP) and Large Language Models (LLMs) to design and scale production intelligence pipelines.

Key Responsibilities:
- Design, train, and deploy transformer-based deep learning models using PyTorch, Hugging Face Transformers, and Sentence-Transformers.
- Build production RAG (Retrieval-Augmented Generation) architectures, vector search systems, and semantic embeddings with LangChain or LlamaIndex.
- Develop data preprocessing pipelines with Python, Pandas, NumPy, and Scikit-Learn for unstructured text data.
- Containerize models using Docker and deploy scalable microservice inference endpoints on AWS using FastAPI and Kubernetes.
- Implement CI/CD pipelines, automated unit testing, model evaluation metrics (F1-score, perplexity, cosine similarity), and drift monitoring.
- Collaborate with cross-functional software engineering teams in an Agile Scrum environment.

Required Qualifications:
- 3+ years experience in Python, PyTorch, and Scikit-Learn.
- Strong practical knowledge of NLP, Deep Learning, Transformers, and LLMs.
- Hands-on experience with Docker, AWS (EC2, S3), Git, and RESTful APIs.
- Experience with databases like PostgreSQL and Redis.
- Excellent communication and analytical problem-solving abilities.""",
            "resume_text": """ALEX MORGAN
Email: alex.morgan.ai@example.com | Phone: (555) 321-7654 | San Francisco, CA
LinkedIn: linkedin.com/in/alexmorgan-ai | GitHub: github.com/alexmorgan-ai

PROFESSIONAL SUMMARY
Senior Machine Learning Engineer with 4+ years of expertise in NLP, Deep Learning, and Transformer architectures. Proven track record deploying semantic search engines, fine-tuning LLMs, and architecting low-latency microservices with PyTorch, FastAPI, and Docker on AWS.

TECHNICAL SKILLS
- Programming Languages: Python, SQL, Bash, C++
- AI & Data Science: Machine Learning, Deep Learning, Natural Language Processing (NLP), Large Language Models (LLMs), Transformers, PyTorch, Scikit-Learn, Hugging Face, Pandas, NumPy
- Cloud & DevOps: Docker, AWS (EC2, S3, ECS), Git, CI/CD, Linux
- Databases & Backend: FastAPI, RESTful APIs, PostgreSQL, Redis, SQLite
- Practices: Agile, Scrum, Unit Testing, System Design

PROFESSIONAL EXPERIENCE
Senior AI Engineer | Apex Intelligence Systems | 2022 - Present
- Architected enterprise semantic document retrieval pipeline using Sentence-Transformers and vector embeddings, improving search precision by 42%.
- Fine-tuned transformer models for sentiment analysis and entity extraction handling 3M+ daily inference queries.
- Containerized NLP inference microservices with Docker and deployed on AWS ECS with auto-scaling, reducing p99 latency to under 45ms.
- Built automated data cleaning and feature engineering pipelines using Pandas, NumPy, and Scikit-Learn.

Machine Learning Engineer | DataVision Labs | 2020 - 2022
- Developed text classification and intent recognition models with PyTorch and Scikit-Learn achieving 94.6% F1-score.
- Created RESTful APIs using FastAPI and integrated Redis caching for prompt management.
- Collaborated in cross-functional Agile sprints with product managers and frontend developers.

EDUCATION
B.S. in Computer Science | University of California, Berkeley | 2016 - 2020
- Focus: Artificial Intelligence & Computational Linguistics"""
        },
        {
            "id": "full-stack-dev",
            "role": "Full Stack Developer",
            "job_title": "Full Stack Software Engineer (React / Node / Python)",
            "job_description": """Job Title: Full Stack Software Engineer
Location: Remote

Overview:
We are looking for a skilled Full Stack Engineer to lead frontend and backend development for our SaaS web application.

Responsibilities:
- Build responsive, modern web applications using React, TypeScript, Next.js, and Tailwind CSS.
- Develop robust, secure RESTful APIs and microservices using Node.js, Express, and Python FastAPI.
- Manage relational and NoSQL databases including PostgreSQL, MySQL, and Redis.
- Deploy applications to cloud infrastructure using Docker, AWS, and automated GitHub Actions CI/CD pipelines.
- Write clean, maintainable code with comprehensive unit testing and participate in Agile code reviews.
- Communicate effectively across teams and demonstrate strong problem-solving skills.

Requirements:
- 3+ years experience with JavaScript, TypeScript, React, and Node.js.
- Strong proficiency in backend development with Python, FastAPI, or Django.
- Experience with Docker, Git, CI/CD, and PostgreSQL.
- Understanding of System Design, Microservices, and REST APIs.""",
            "resume_text": """JORDAN REED
Email: jordan.reed.dev@example.com | New York, NY
Portfolio: jordanreed.dev | GitHub: github.com/jordanreed

SUMMARY
Full Stack Developer with 4 years of experience crafting modern web applications and resilient distributed systems. Specialized in TypeScript, React, Node.js, Python, and cloud deployments on AWS.

TECHNICAL SKILLS
- Languages: JavaScript, TypeScript, Python, HTML5, CSS3, SQL
- Frontend: React, Next.js, Tailwind CSS, Redux
- Backend: Node.js, Express, FastAPI, RESTful APIs, Microservices
- Databases: PostgreSQL, MongoDB, Redis, SQLite
- Cloud & Tools: AWS, Docker, Git, CI/CD, Linux, Unit Testing, Agile

WORK EXPERIENCE
Full Stack Engineer | CloudScale Tech | 2022 - Present
- Built high-performance responsive web dashboard using React, TypeScript, and Tailwind CSS, increasing user engagement by 35%.
- Engineered asynchronous microservices backend with Node.js, Express, and FastAPI handling 10,000+ simultaneous WebSocket connections.
- Integrated PostgreSQL with connection pooling and optimized database queries, reducing API response times by 50%.
- Configured automated GitHub Actions CI/CD pipelines and Docker containers for seamless deployment to AWS.

Frontend Developer | PixelCraft Solutions | 2020 - 2022
- Developed modular React components and single-page applications.
- Collaborated with UX designers to implement accessible, responsive interfaces using Tailwind CSS and HTML5.
- Participated in daily Agile standups and sprint planning.

EDUCATION
B.S. in Software Engineering | New York University | 2016 - 2020"""
        },
        {
            "id": "devops-engineer",
            "role": "DevOps & Cloud Engineer",
            "job_title": "DevOps / Infrastructure Platform Engineer",
            "job_description": """Job Title: DevOps & Infrastructure Engineer
Location: Hybrid

Key Duties:
- Architect and manage cloud infrastructure on AWS and Google Cloud Platform using Terraform.
- Orchestrate container workloads with Kubernetes (EKS/GKE) and Docker.
- Build continuous integration and deployment pipelines (CI/CD) using GitHub Actions, Jenkins, and Helm.
- Implement observability and monitoring stacks with Prometheus, Grafana, and Linux system logging.
- Ensure infrastructure security, high availability, and disaster recovery.
- Collaborate with backend software teams on system design and release automation.

Requirements:
- Strong Linux administration and Bash/Python scripting.
- Production experience with Kubernetes, Docker, and Terraform.
- Hands-on experience with AWS, CI/CD pipelines, and Git.""",
            "resume_text": """SAMIRA KHAN
DevOps Engineer | Austin, TX | samira.khan.devops@example.com

PROFESSIONAL SUMMARY
DevOps and Cloud Engineer with 3+ years building resilient cloud foundations, Kubernetes clusters, and automated CI/CD pipelines.

CORE COMPETENCIES
- Cloud: AWS, Google Cloud Platform (GCP)
- Containerization & Orchestration: Docker, Kubernetes, Helm
- IaC & Automation: Terraform, Bash, Python, Linux
- CI/CD & Version Control: CI/CD, Git, GitHub Actions, Jenkins
- Monitoring: Prometheus, Grafana
- Practices: Agile, System Design, High Availability

EXPERIENCE
Cloud Infrastructure Engineer | Nexus Cloud Systems | 2022 - Present
- Provisioned multi-region AWS infrastructure using Terraform IaC modules.
- Managed Kubernetes clusters running 200+ containerized microservices.
- Constructed automated CI/CD delivery pipelines with GitHub Actions and Docker.
- Automated system health monitoring with Prometheus and custom Grafana dashboards.

Linux Systems Administrator | Enterprise Hosting | 2021 - 2022
- Managed fleet of 150+ Linux servers, configuring security hardening and automated Bash cron scripts.
- Implemented Git version control workflows for operational automation.

EDUCATION
B.S. in Information Technology | University of Texas at Austin | 2017 - 2021"""
        }
    ]
    return samples
