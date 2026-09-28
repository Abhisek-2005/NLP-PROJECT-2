import re
from typing import Dict, List, Set, Tuple

# Comprehensive taxonomy of industry skills, aliases, and categories
SKILL_TAXONOMY: Dict[str, Dict[str, any]] = {
    # Programming Languages
    "Python": {"category": "Programming Languages", "aliases": ["python", "python3", "py"]},
    "JavaScript": {"category": "Programming Languages", "aliases": ["javascript", "js", "ecmascript", "es6", "es2020"]},
    "TypeScript": {"category": "Programming Languages", "aliases": ["typescript", "ts"]},
    "Java": {"category": "Programming Languages", "aliases": ["java", "jdk", "jvm", "j2ee"]},
    "C++": {"category": "Programming Languages", "aliases": ["c++", "cpp"]},
    "C#": {"category": "Programming Languages", "aliases": ["c#", "csharp", ".net c#"]},
    "C": {"category": "Programming Languages", "aliases": ["c lang", "c language"]},
    "Go": {"category": "Programming Languages", "aliases": ["golang", "go lang"]},
    "Rust": {"category": "Programming Languages", "aliases": ["rust", "rustlang"]},
    "Ruby": {"category": "Programming Languages", "aliases": ["ruby", "ruby on rails"]},
    "PHP": {"category": "Programming Languages", "aliases": ["php", "php8"]},
    "Swift": {"category": "Programming Languages", "aliases": ["swift", "swiftui"]},
    "Kotlin": {"category": "Programming Languages", "aliases": ["kotlin"]},
    "SQL": {"category": "Programming Languages", "aliases": ["sql", "transact-sql", "t-sql", "pl/sql"]},
    "R": {"category": "Programming Languages", "aliases": ["r lang", "r language", "r-project"]},
    "Scala": {"category": "Programming Languages", "aliases": ["scala"]},
    "Bash": {"category": "Programming Languages", "aliases": ["bash", "shell", "powershell", "shell scripting"]},

    # Frameworks & Libraries
    "React": {"category": "Frameworks & Libraries", "aliases": ["react", "react.js", "reactjs"]},
    "Next.js": {"category": "Frameworks & Libraries", "aliases": ["next.js", "nextjs", "next"]},
    "Node.js": {"category": "Frameworks & Libraries", "aliases": ["node.js", "nodejs", "node"]},
    "Express": {"category": "Frameworks & Libraries", "aliases": ["express", "express.js", "expressjs"]},
    "FastAPI": {"category": "Frameworks & Libraries", "aliases": ["fastapi", "fast-api"]},
    "Django": {"category": "Frameworks & Libraries", "aliases": ["django", "django rest framework", "drf"]},
    "Flask": {"category": "Frameworks & Libraries", "aliases": ["flask"]},
    "Spring Boot": {"category": "Frameworks & Libraries", "aliases": ["spring boot", "springboot", "spring framework", "spring"]},
    "Vue.js": {"category": "Frameworks & Libraries", "aliases": ["vue", "vue.js", "vuejs", "vue3"]},
    "Angular": {"category": "Frameworks & Libraries", "aliases": ["angular", "angularjs", "angular 2+"]},
    "Tailwind CSS": {"category": "Frameworks & Libraries", "aliases": ["tailwind", "tailwindcss", "tailwind-css"]},
    "Bootstrap": {"category": "Frameworks & Libraries", "aliases": ["bootstrap", "bootstrap 5"]},
    "HTML5 / CSS3": {"category": "Frameworks & Libraries", "aliases": ["html", "html5", "css", "css3", "sass", "scss"]},
    "GraphQL": {"category": "Frameworks & Libraries", "aliases": ["graphql", "apollo graphql"]},

    # AI, ML & Data Science
    "Machine Learning": {"category": "AI & Data Science", "aliases": ["machine learning", "ml", "statistical learning"]},
    "Deep Learning": {"category": "AI & Data Science", "aliases": ["deep learning", "neural networks", "dl", "ann", "cnn", "rnn", "lstm"]},
    "Natural Language Processing": {"category": "AI & Data Science", "aliases": ["nlp", "natural language processing", "text mining", "computational linguistics"]},
    "Computer Vision": {"category": "AI & Data Science", "aliases": ["computer vision", "cv", "image processing", "opencv"]},
    "Large Language Models": {"category": "AI & Data Science", "aliases": ["llm", "large language models", "llms", "gpt", "rag", "retrieval-augmented generation", "langchain", "llamaindex", "generative ai", "genai"]},
    "Transformers": {"category": "AI & Data Science", "aliases": ["transformers", "huggingface", "hugging face", "bert", "sentence-transformers"]},
    "PyTorch": {"category": "AI & Data Science", "aliases": ["pytorch", "torch"]},
    "TensorFlow": {"category": "AI & Data Science", "aliases": ["tensorflow", "tf", "keras"]},
    "Scikit-Learn": {"category": "AI & Data Science", "aliases": ["scikit-learn", "sklearn"]},
    "Pandas": {"category": "AI & Data Science", "aliases": ["pandas"]},
    "NumPy": {"category": "AI & Data Science", "aliases": ["numpy"]},
    "Data Preprocessing": {"category": "AI & Data Science", "aliases": ["data preprocessing", "data cleaning", "feature engineering", "eda", "exploratory data analysis"]},
    "Model Evaluation": {"category": "AI & Data Science", "aliases": ["model evaluation", "cross-validation", "hyperparameter tuning", "roc-auc", "f1-score"]},
    "Big Data": {"category": "AI & Data Science", "aliases": ["spark", "apache spark", "pyspark", "hadoop", "databricks"]},

    # Cloud & DevOps
    "AWS": {"category": "Cloud & DevOps", "aliases": ["aws", "amazon web services", "ec2", "s3", "lambda", "ecs", "eks", "rds"]},
    "Azure": {"category": "Cloud & DevOps", "aliases": ["azure", "microsoft azure", "azure devops"]},
    "Google Cloud Platform": {"category": "Cloud & DevOps", "aliases": ["gcp", "google cloud", "google cloud platform", "bigquery"]},
    "Docker": {"category": "Cloud & DevOps", "aliases": ["docker", "containerization", "docker-compose", "containers"]},
    "Kubernetes": {"category": "Cloud & DevOps", "aliases": ["kubernetes", "k8s"]},
    "CI/CD": {"category": "Cloud & DevOps", "aliases": ["ci/cd", "ci-cd", "continuous integration", "continuous deployment", "github actions", "gitlab ci", "jenkins"]},
    "Terraform": {"category": "Cloud & DevOps", "aliases": ["terraform", "iac", "infrastructure as code"]},
    "Linux": {"category": "Cloud & DevOps", "aliases": ["linux", "ubuntu", "debian", "centos", "redhat"]},
    "Git": {"category": "Cloud & DevOps", "aliases": ["git", "github", "gitlab", "bitbucket", "version control"]},

    # Databases & Storage
    "PostgreSQL": {"category": "Databases & Storage", "aliases": ["postgresql", "postgres", "psql"]},
    "MySQL": {"category": "Databases & Storage", "aliases": ["mysql", "mariadb"]},
    "MongoDB": {"category": "Databases & Storage", "aliases": ["mongodb", "mongo", "nosql"]},
    "Redis": {"category": "Databases & Storage", "aliases": ["redis", "in-memory cache"]},
    "SQLite": {"category": "Databases & Storage", "aliases": ["sqlite", "sqlite3"]},
    "Elasticsearch": {"category": "Databases & Storage", "aliases": ["elasticsearch", "elastic search", "opensearch"]},
    "Snowflake": {"category": "Databases & Storage", "aliases": ["snowflake", "data warehouse"]},

    # Architecture & Practices
    "RESTful APIs": {"category": "Architecture & Practices", "aliases": ["rest", "restful", "rest api", "rest apis", "restful api"]},
    "Microservices": {"category": "Architecture & Practices", "aliases": ["microservices", "microservice architecture", "distributed systems"]},
    "Agile / Scrum": {"category": "Architecture & Practices", "aliases": ["agile", "scrum", "kanban", "sprint planning", "jira"]},
    "System Design": {"category": "Architecture & Practices", "aliases": ["system design", "software architecture", "scalability", "high availability"]},
    "Unit Testing": {"category": "Architecture & Practices", "aliases": ["unit testing", "tdd", "test-driven development", "pytest", "jest", "mocking"]},

    # Soft Skills
    "Communication": {"category": "Soft Skills", "aliases": ["communication", "verbal communication", "written communication", "presentation skills"]},
    "Leadership": {"category": "Soft Skills", "aliases": ["leadership", "team lead", "tech lead", "lead", "mentorship", "mentoring"]},
    "Problem Solving": {"category": "Soft Skills", "aliases": ["problem solving", "analytical thinking", "critical thinking", "troubleshooting"]},
    "Collaboration": {"category": "Soft Skills", "aliases": ["teamwork", "cross-functional collaboration", "cross-functional teams", "collaboration"]},
    "Time Management": {"category": "Soft Skills", "aliases": ["time management", "prioritization", "multitasking"]},
}

class SkillExtractionService:
    """Extracts, categorizes, and matches skills from textual documents."""

    def __init__(self):
        # Precompile regex search patterns for maximum speed and accuracy
        self.compiled_skills: List[Tuple[str, str, List[re.Pattern]]] = []
        for skill_name, info in SKILL_TAXONOMY.items():
            category = info["category"]
            patterns = []
            for alias in info["aliases"]:
                # Escape special regex chars like ++, #, ., -
                escaped = re.escape(alias)
                # Word boundary check tailored for programming tokens
                # \b doesn't always handle c++ or .net properly, so we use lookbehind/lookahead
                pattern = re.compile(rf"(?<![a-zA-Z0-9_\.]){escaped}(?![a-zA-Z0-9_])", re.IGNORECASE)
                patterns.append(pattern)
            self.compiled_skills.append((skill_name, category, patterns))

    def extract_skills(self, text: str) -> List[Dict[str, any]]:
        """Extracts recognized skills and their categories from text."""
        detected = []
        seen = set()

        for skill_name, category, patterns in self.compiled_skills:
            if skill_name in seen:
                continue
            for pat in patterns:
                if pat.search(text):
                    detected.append({
                        "name": skill_name,
                        "category": category,
                        "importance": "Important"
                    })
                    seen.add(skill_name)
                    break

        return detected

    def compare_skills(
        self,
        resume_skills: List[Dict[str, any]],
        job_skills: List[Dict[str, any]]
    ) -> Tuple[List[Dict[str, any]], List[Dict[str, any]], float]:
        """
        Compares skills between resume and job description.
        Returns:
            matched_skills: list of skills present in both
            missing_skills: list of job skills absent from resume
            skill_score: percentage 0.0 - 100.0
        """
        resume_names = {s["name"].lower() for s in resume_skills}
        job_names = {s["name"].lower() for s in job_skills}

        matched = []
        missing = []

        # Technical categories are treated as critical/high priority
        critical_categories = {"Programming Languages", "AI & Data Science", "Frameworks & Libraries", "Cloud & DevOps"}

        for job_skill in job_skills:
            s_name = job_skill["name"]
            is_matched = s_name.lower() in resume_names
            cat = job_skill.get("category", "General")
            importance = "Critical" if cat in critical_categories else "Important"

            skill_entry = {
                "name": s_name,
                "category": cat,
                "is_matched": is_matched,
                "importance": importance
            }

            if is_matched:
                matched.append(skill_entry)
            else:
                missing.append(skill_entry)

        # Calculate weighted skill match score
        total_job = len(job_skills)
        if total_job == 0:
            # If no explicit taxonomy skills found in job description, fallback to neutral
            skill_score = 75.0 if len(resume_skills) > 0 else 50.0
        else:
            # Critical skills carry 1.5x weight
            total_points = sum(1.5 if s.get("category") in critical_categories else 1.0 for s in job_skills)
            earned_points = sum(1.5 if s.get("category") in critical_categories else 1.0 for s in matched)
            skill_score = round(min(100.0, (earned_points / max(1.0, total_points)) * 100.0), 2)

        return matched, missing, skill_score
