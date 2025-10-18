import uuid
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction

# Replace 'myapp' with the actual name of your Django app containing the models
from API.models import (
    Sector, Career, Introduction, Responsibility, Education, Skill, 
    Specialization, Certification, Roadmap, Phase
) 

class Command(BaseCommand):
    help = 'Populates the database with detailed Information Technology career data (9 roles).'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting IT career data population...'))

        # --- 1. PRE-POPULATE LOOKUP DATA (Skills, Education, Certs) ---
        
        self.stdout.write(self.style.NOTICE('1. Creating global Skills, Education, and Certifications...'))

        # Create all unique skills needed across all IT careers
        skills_data = [
            # Core Tech Skills
            ('Python Programming', 'Mastery of Python for scripting, data manipulation (Pandas), or backend development (Django/Flask).'),
            ('System Architecture Design', 'Ability to design scalable, distributed, and high-availability systems.'),
            ('SQL & Database Management', 'Expertise in relational database querying, modeling, and optimization (PostgreSQL/MySQL).'),
            ('Cybersecurity Fundamentals', 'Knowledge of security principles, threat modeling, and defensive coding practices.'),
            ('CI/CD & Automation', 'Tools and practices for automated build, test, and deployment (Jenkins, GitLab CI, Terraform).'),
            ('Cloud Architecture', 'Designing and managing services on major cloud platforms (AWS, Azure, GCP).'),
            ('Project Management', 'Agile methodologies, sprint planning, and coordinating development efforts.'),
            # Data/AI Skills
            ('MLOps & Model Deployment', 'Practices for deploying, monitoring, and maintaining machine learning models in production.'),
            ('Data Visualization & BI', 'Using tools like Tableau/PowerBI to create clear, actionable data narratives.'),
            # Security Skills
            ('Digital Forensics', 'Techniques for investigating and recovering material found in digital devices.'),
            ('Risk Quantification', 'Methodologies for measuring and managing technical and operational risk.'),
            ('Advanced Mathematics', 'Probability, statistics, and linear algebra crucial for advanced AI/ML.'),
            # Added for new roles
            ('Networking & TCP/IP', 'Deep understanding of network protocols, routing, and switching infrastructure.'),
            ('Linux Administration', 'Competency in command-line operations, scripting, and server management.'),
            ('Human-Computer Interaction (HCI)', 'Principles governing the design of user interfaces and user experience.'),
            ('Wireframing & Prototyping', 'Creating low-fidelity wireframes and interactive high-fidelity prototypes (e.g., Figma, Sketch).'),
            ('User Research & Testing', 'Methods for gathering data on user needs, behaviors, and pain points.'),
            ('Business Strategy & Market Analysis', 'Ability to define market opportunities, competitive landscapes, and long-term product vision.'),
        ]
        skills_map = {name: Skill.objects.get_or_create(name=name, description=desc)[0] for name, desc in skills_data}
        self.stdout.write(self.style.SUCCESS(f'   Created {len(skills_map)} skills.'))

        # Create all unique education options
        education_data = [
            ('Bachelor of Computer Science', 'Core foundation for programming, systems design, and algorithms.', 7, 4.0),
            ('BSc Cloud Computing / DevOps', 'Cloud architectures, distributed systems, and modern software delivery practices.', 7, 4.0),
            ('Master of Science (MSc) Machine Learning', 'Advanced machine learning, deep learning, and deployment of AI systems.', 9, 2.0),
            # Added for new roles
            ('Bachelor of Design / HCI', 'Focus on human-centered design, usability, and visual aesthetics.', 7, 4.0),
            ('Master of Business Administration (MBA)', 'Advanced training in business strategy, finance, and leadership.', 9, 2.0),
        ]
        education_map = {name: Education.objects.get_or_create(name=name, description=desc, nqf_level=nqf, duration_years=Decimal(duration))[0] 
                         for name, desc, nqf, duration in education_data}
        self.stdout.write(self.style.SUCCESS(f'   Created {len(education_map)} education options.'))

        # Create certifications (simple model)
        certifications_data = [
            ('AWS Certified Solutions Architect', 'Validate expertise in designing and deploying scalable, robust cloud systems.'),
            ('CompTIA Security+', 'Foundation certification covering core security functions.'),
            ('Certified Ethical Hacker (CEH)', 'Certifies skills in penetration testing and defensive security.'),
            # Added for new roles
            ('Cisco Certified Network Associate (CCNA)', 'Entry-level certification covering foundational networking concepts and implementation.'),
            ('Certified Information Systems Security Professional (CISSP)', 'Globally recognized certification for senior security practitioners.'),
            ('Certified Scrum Product Owner (CSPO)', 'Certifies understanding of the Scrum framework from the Product Owner perspective.'),
        ]
        cert_map = {name: Certification.objects.get_or_create(name=name, description=desc)[0] for name, desc in certifications_data}
        self.stdout.write(self.style.SUCCESS(f'   Created {len(cert_map)} certifications.'))


        # --- 2. CREATE SECTOR ---
        it_sector, _ = Sector.objects.get_or_create(
            name="Information Technology",
            defaults={
                "description": "Technology and software development careers driving digital innovation, focusing on system design, data, and security."
            }
        )
        self.stdout.write(self.style.SUCCESS('2. Created Sector: Information Technology.'))


        # --- 3. CAREER DATA DEFINITION & POPULATION ---

        career_data = {
            "Software Engineer": {
                "overview": "Design, develop, and maintain robust and scalable applications that power modern software systems.",
                "salary": 1305000.00,
                "outlook": "Strong growth across all digital industries and technological advancements.",
                "intro": {
                    "content": "The Software Engineer is the backbone of the digital world. This role involves translating user needs into functional, high-performance code, managing the entire software development lifecycle (SDLC), and working across multiple technology stacks. Proficiency in algorithms, data structures, and system design is paramount.",
                    "years": 4, "months": 0
                },
                "responsibilities": [
                    "Designing and implementing new software features and enhancements using modern programming languages.",
                    "Writing clean, maintainable, and well-documented code that adheres to industry standards.",
                    "Conducting rigorous unit and integration testing to ensure code quality and system reliability.",
                    "Collaborating with product managers and designers to define specifications and deliver features within sprint cycles.",
                    "Participating in code reviews to maintain high quality and knowledge sharing within the team.",
                    "Troubleshooting and debugging production issues across distributed systems.",
                    "Optimizing application performance, latency, and scalability, often involving database query tuning.",
                    "Contributing to architectural decisions and selecting appropriate technologies for new projects.",
                    "Managing version control and contributing to CI/CD pipelines.",
                    "Mentoring junior developers and helping to onboard new team members."
                ],
                "specializations": [
                    ("Frontend Developer", "Specialize in building interactive web interfaces using modern frameworks (React, Vue, Angular)."),
                    ("Backend Developer", "Design scalable backend systems, APIs, and business logic often using Python, Java, or Go."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: Foundation",
                        "order": 1,
                        "description": "Complete Bachelor of Computer Science, achieve mastery of algorithms, data structures, and at least two programming languages. Understand core system architecture fundamentals.",
                        "education": ["Bachelor of Computer Science"],
                        "skills": ["Python Programming", "System Architecture Design", "SQL & Database Management", "Cybersecurity Fundamentals"],
                        "certifications": [],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: Full-Stack Competency",
                        "order": 2,
                        "description": "Master SQL for efficient data handling. Build a robust portfolio demonstrating both Frontend and Backend skills. Implement basic security protocols.",
                        "education": ["BSc Cloud Computing / DevOps"],
                        "skills": ["SQL & Database Management", "CI/CD & Automation", "Cloud Architecture", "Project Management"],
                        "certifications": [],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 3: Scale & Delivery",
                        "order": 3,
                        "description": "Focus on microservices architecture, performance tuning, and utilizing CI/CD Automation. Achieve cloud certification. Apply basic principles of MLOps for advanced features.",
                        "education": [],
                        "skills": ["MLOps & Model Deployment", "Project Management"],
                        "certifications": ['AWS Certified Solutions Architect'],
                        "specializations": ["Frontend Developer", "Backend Developer"],
                    },
                    {
                        "name": "Phase 4: Leadership",
                        "order": 4,
                        "description": "Transition to Principal Engineer or Engineering Manager, responsible for complex systems design, architectural governance, and team leadership. Drive technical strategy.",
                        "education": [],
                        "skills": [],
                        "certifications": [],
                        "specializations": [],
                    }
                ]
            },
            
            "Data Analyst": {
                "overview": "Collect, process, and analyze complex datasets to produce actionable business insights and inform strategic decisions.",
                "salary": 986000.00,
                "outlook": "Rapid growth driven by data-driven decision making across all industries.",
                "intro": {
                    "content": "Data Analysts act as translators, converting raw numbers into clear narratives. They are responsible for cleaning, transforming, and modeling data, then presenting their findings to stakeholders using compelling visualizations and reports.",
                    "years": 3, "months": 0
                },
                "responsibilities": [
                    "Developing and executing complex SQL queries to extract data from various database sources.",
                    "Cleaning and preprocessing data using Python Programming (Pandas, NumPy) to ensure accuracy and consistency.",
                    "Designing and maintaining interactive dashboards and reports using Data Visualization & BI tools.",
                    "Conducting exploratory data analysis (EDA) to identify trends, correlations, and anomalies.",
                    "Performing statistical analysis (e.g., A/B testing, regression) to support business hypotheses.",
                    "Presenting findings and strategic recommendations to non-technical stakeholders clearly and concisely.",
                    "Collaborating with data engineers and software developers to improve data collection infrastructure.",
                    "Creating and managing data dictionaries and documentation for datasets.",
                    "Monitoring key performance indicators (KPIs) and alerting teams to significant shifts.",
                    "Contributing to System Architecture Design of data warehousing solutions."
                ],
                "specializations": [
                    ("Business Data Analyst", "Focus on business intelligence, market trends, and data-driven strategy development."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: Technical Base",
                        "order": 1,
                        "description": "Obtain a quantitative degree. Master Python Programming for data manipulation (Pandas, NumPy) and statistics. Master foundational SQL & Database Management concepts.",
                        "education": ["Bachelor of Computer Science"],
                        "skills": ["Python Programming", "SQL & Database Management", "Data Visualization & BI", "System Architecture Design"],
                        "certifications": [],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: BI & Reporting",
                        "order": 2,
                        "description": "Achieve deep proficiency in advanced SQL techniques. Master Data Visualization & BI tools (Tableau, PowerBI) to build insightful dashboards. Learn basic data pipeline implementation.",
                        "education": ["BSc Cloud Computing / DevOps"],
                        "skills": ["CI/CD & Automation", "Cloud Architecture", "Project Management"],
                        "certifications": [],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 3: Applied Strategy",
                        "order": 3,
                        "description": "Secure an Analyst role; focus on interpreting complex experiments and providing actionable recommendations. Apply basic MLOps concepts.",
                        "education": [],
                        "skills": ["MLOps & Model Deployment", "Cybersecurity Fundamentals"],
                        "certifications": [],
                        "specializations": ["Business Data Analyst"],
                    },
                    {
                        "name": "Phase 4: Strategy Leadership",
                        "order": 4,
                        "description": "Advance to Analytics Manager or Business Data Analyst leadership, leading data strategy, predictive modeling projects, and driving cross-functional decisions.",
                        "education": [],
                        "skills": [],
                        "certifications": [],
                        "specializations": [],
                    }
                ]
            },
            
            # --- 3. NEW CAREER: CYBERSECURITY SPECIALIST ---
            "Cybersecurity Specialist": {
                "overview": "Protect computer systems, networks, and data from digital attacks, breaches, and unauthorized access.",
                "salary": 1377500.00,
                "outlook": "One of the fastest-growing technology fields due to increasing threat complexity.",
                "intro": {
                    "content": "Cybersecurity Specialists are the digital guardians. They analyze security posture, implement defensive measures, conduct penetration testing, manage incident response, and ensure compliance with regulatory standards to safeguard sensitive information.",
                    "years": 4, "months": 0
                },
                "responsibilities": [
                    "Monitoring security access and using SIEM (Security Information and Event Management) tools to detect threats.",
                    "Implementing, maintaining, and auditing firewalls, VPNs, and intrusion detection systems.",
                    "Conducting regular vulnerability assessments and penetration tests.",
                    "Developing and maintaining security policies, procedures, and best practices.",
                    "Managing incident response, including containment, eradication, and recovery from security breaches.",
                    "Ensuring all systems comply with relevant regulatory standards (e.g., GDPR, HIPAA).",
                    "Securing cloud infrastructure and managing identity and access management (IAM).",
                    "Scripting security tools and automation tasks using Python Programming.",
                    "Performing Digital Forensics on compromised systems to determine the root cause of attacks.",
                    "Educating and training staff on security awareness and best practices."
                ],
                "specializations": [
                    ("Penetration Tester", "Simulating cyber attacks (ethical hacking) to identify and evaluate system weaknesses."),
                    ("Cloud Security Architect", "Design and implement secure cloud infrastructures and compliance controls."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: Core Systems",
                        "order": 1,
                        "description": "Obtain a Bachelor of Computer Science. Master networking, OS fundamentals, and scripting with Python. Understand System Architecture Design and SQL.",
                        "education": ["Bachelor of Computer Science"],
                        "skills": ["Python Programming", "Cybersecurity Fundamentals", "Networking & TCP/IP", "Linux Administration"],
                        "certifications": ['CompTIA Security+'],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: Defensive Mastery",
                        "order": 2,
                        "description": "Gain foundational security certifications. Master threat detection, log analysis, and SIEM tool use. Implement secure CI/CD & Automation principles.",
                        "education": ["BSc Cloud Computing / DevOps"],
                        "skills": ["CI/CD & Automation", "Cloud Architecture", "Digital Forensics", "Risk Quantification"],
                        "certifications": [],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 3: Offensive Specialization",
                        "order": 3,
                        "description": "Pursue the Penetration Tester track (e.g., CEH) or the Cloud Security Architect track. Deepen Digital Forensics and incident response skills.",
                        "education": [],
                        "skills": ["Project Management", "System Architecture Design"],
                        "certifications": ['Certified Ethical Hacker (CEH)', 'CISSP'],
                        "specializations": ["Penetration Tester", "Cloud Security Architect"],
                    },
                    {
                        "name": "Phase 4: CISO Track",
                        "order": 4,
                        "description": "Transition to an InfoSec Manager or Chief Information Security Officer (CISO). Set corporate security policy and lead enterprise security strategy.",
                        "education": [],
                        "skills": [],
                        "certifications": [],
                        "specializations": [],
                    }
                ]
            },

            # --- 4. NEW CAREER: CLOUD ARCHITECT ---
            "Cloud Architect": {
                "overview": "Design, build, and operate secure, scalable, and cost-optimized cloud solutions and platforms for modern applications.",
                "salary": 1885000.00,
                "outlook": "Very strong demand as organizations rapidly migrate to and optimize cloud-first architectures.",
                "intro": {
                    "content": "A Cloud Architect is a top-tier systems designer focused on infrastructure. They evaluate business requirements and translate them into a technical design using cloud provider services (AWS, Azure, GCP), ensuring solutions meet requirements for security, performance, cost, and resiliency.",
                    "years": 5, "months": 0
                },
                "responsibilities": [
                    "Designing well-architected frameworks (security, performance, cost) for new cloud deployments.",
                    "Implementing Infrastructure as Code (IaC) using tools like Terraform or CloudFormation.",
                    "Managing complex networking, identity, and access management (IAM) within multi-cloud environments.",
                    "Optimizing cloud expenditure (FinOps) and resource utilization across departments.",
                    "Ensuring robust Cloud Architecture security, governance, and compliance.",
                    "Developing and maintaining deployment pipelines using CI/CD & Automation.",
                    "Providing technical guidance and troubleshooting for platform engineers and developers.",
                    "Documenting architectural decisions, technical standards, and deployment procedures.",
                    "Utilizing System Architecture Design principles for microservices and distributed systems.",
                    "Conducting architectural review of applications before production deployment."
                ],
                "specializations": [
                    ("Multi-Cloud Specialist", "Designing and managing solutions across two or more major cloud providers (e.g., AWS and Azure)."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: Cloud Foundation",
                        "order": 1,
                        "description": "Complete a BSc in Cloud Computing / DevOps. Understand core networking, virtualization, and Cybersecurity Fundamentals. Master basic scripting with Python.",
                        "education": ["BSc Cloud Computing / DevOps"],
                        "skills": ["Cloud Architecture", "Cybersecurity Fundamentals", "Python Programming", "Networking & TCP/IP", "Linux Administration"],
                        "certifications": [],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: Architectural Mastery",
                        "order": 2,
                        "description": "Obtain Associate-level Cloud Vendor Certifications. Master Cloud Architecture, designing fault-tolerant systems. Master CI/CD & Automation and IaC tools.",
                        "education": ["Bachelor of Computer Science"],
                        "skills": ["CI/CD & Automation", "System Architecture Design", "SQL & Database Management"],
                        "certifications": ['AWS Certified Solutions Architect'],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 3: Security & Optimization",
                        "order": 3,
                        "description": "Obtain Professional-level Cloud Vendor Certifications. Focus on advanced security (Cloud Security Architect) and optimizing cloud costs (FinOps).",
                        "education": [],
                        "skills": ["Digital Forensics", "Risk Quantification", "Project Management"],
                        "certifications": ['CISSP'],
                        "specializations": ["Multi-Cloud Specialist"],
                    },
                    {
                        "name": "Phase 4: Enterprise Strategy",
                        "order": 4,
                        "description": "Lead the Cloud Center of Excellence (CCoE), setting the organization's entire cloud migration and multi-cloud strategy.",
                        "education": [],
                        "skills": [],
                        "certifications": [],
                        "specializations": [],
                    }
                ]
            },

            # --- 5. NEW CAREER: AI ENGINEER ---
            "AI Engineer": {
                "overview": "Build, deploy, and productionize machine learning models, artificial intelligence solutions, and complex data science systems.",
                "salary": 2175000.00,
                "outlook": "Rapid growth, extremely high demand for engineers who can deploy and scale AI solutions.",
                "intro": {
                    "content": "AI Engineers bridge the gap between pure data science and production software. They possess strong mathematical foundations but prioritize engineering practices: model training, deployment, monitoring, and integration into existing software systems.",
                    "years": 5, "months": 0
                },
                "responsibilities": [
                    "Designing and implementing scalable machine learning (ML) model training and inference pipelines.",
                    "Writing production-grade code in Python Programming for data processing and model serving.",
                    "Developing expertise in MLOps & Model Deployment for continuous integration and monitoring of models.",
                    "Collaborating with Data Scientists to refactor research code into efficient production systems.",
                    "Selecting and managing appropriate data storage and processing technologies (SQL & Database Management).",
                    "Designing the System Architecture Design for distributed ML services and APIs.",
                    "Benchmarking model performance, latency, and resource consumption.",
                    "Utilizing cloud services (Cloud Architecture) for training and deployment at scale.",
                    "Ensuring model fairness, interpretability, and ethical AI practices.",
                    "Staying current with the latest deep learning and AI research and frameworks."
                ],
                "specializations": [
                    ("Computer Vision Specialist", "Focus on ML models for image/video systems, object detection, and perception tasks."),
                    ("NLP Specialist", "Focus on natural language processing, text analysis, and large language models (LLMs)."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: Advanced Education",
                        "order": 1,
                        "description": "Obtain an MSc Machine Learning or equivalent. Master deep learning, reinforcement learning, and advanced linear algebra.",
                        "education": ["Master of Science (MSc) Machine Learning"],
                        "skills": ["Advanced Mathematics", "Python Programming", "System Architecture Design", "SQL & Database Management"],
                        "certifications": [],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: Engineering Practice",
                        "order": 2,
                        "description": "Secure an AI Engineer role. Develop expertise in MLOps & Model Deployment, focusing on continuous training and performance monitoring.",
                        "education": ["Bachelor of Computer Science"],
                        "skills": ["MLOps & Model Deployment", "Cloud Architecture", "CI/CD & Automation", "Data Visualization & BI"],
                        "certifications": [],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 3: Technical Specialization",
                        "order": 3,
                        "description": "Master System Architecture Design for high-throughput inference systems. Focus on a high-value area like Computer Vision or NLP. Utilize Cloud Architecture services for global scale.",
                        "education": [],
                        "skills": ["Cybersecurity Fundamentals", "Project Management"],
                        "certifications": [],
                        "specializations": ["Computer Vision Specialist", "NLP Specialist"],
                    },
                    {
                        "name": "Phase 4: Research/Director Level",
                        "order": 4,
                        "description": "Lead ML research or become a Director of AI, defining the technological roadmap and ethical governance for AI solutions.",
                        "education": [],
                        "skills": [],
                        "certifications": [],
                        "specializations": [],
                    }
                ]
            },

            # --- 6. NEW CAREER: DEVOPS ENGINEER ---
            "DevOps Engineer": {
                "overview": "Bridge development and operations by managing CI/CD pipelines, automating infrastructure, and improving system reliability.",
                "salary": 1522500.00,
                "outlook": "High demand, essential for modern software delivery, speed, and reliability.",
                "intro": {
                    "content": "DevOps Engineers focus on culture, automation, measurement, and sharing. They are experts in tools that automate the software delivery lifecycle, manage containerized applications, and ensure the operational health and observability of production systems.",
                    "years": 4, "months": 0
                },
                "responsibilities": [
                    "Designing, implementing, and maintaining fully automated CI/CD & Automation pipelines (e.g., Jenkins, GitLab CI).",
                    "Managing infrastructure-as-code (IaC) with tools like Terraform, Ansible, or CloudFormation.",
                    "Deploying and managing containerized applications using Docker and Kubernetes.",
                    "Monitoring system performance, setting up alerts, and implementing logging and tracing tools.",
                    "Collaborating with development teams to ensure applications are designed for deployment and scalability.",
                    "Implementing security controls and continuous vulnerability scanning in the CI/CD pipeline (Cybersecurity Fundamentals).",
                    "Performing on-call duties for incident response and improving system reliability (SRE principles).",
                    "Managing SQL & Database Management instances for persistent storage and backups.",
                    "Designing high-availability and disaster recovery solutions using Cloud Architecture.",
                    "Utilizing Python Programming and shell scripting for system automation."
                ],
                "specializations": [
                    ("Kubernetes and Containerization", "Specialize in deploying and managing containerized applications at massive scale."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: Systems Foundation",
                        "order": 1,
                        "description": "Complete a BSc in Cloud Computing / DevOps. Master networking, Linux administration, and Cybersecurity Fundamentals. Master Python Programming and basic SQL.",
                        "education": ["BSc Cloud Computing / DevOps"],
                        "skills": ["CI/CD & Automation", "Cloud Architecture", "Python Programming", "Linux Administration", "Cybersecurity Fundamentals", "Networking & TCP/IP"],
                        "certifications": [],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: Automation Mastery",
                        "order": 2,
                        "description": "Develop deep expertise in CI/CD Automation using tools and IaC. Master Cloud Architecture principles and System Architecture Design for reliability.",
                        "education": ["Bachelor of Computer Science"],
                        "skills": ["System Architecture Design", "Project Management", "SQL & Database Management"],
                        "certifications": ['AWS Certified Solutions Architect'],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 3: Cloud & Containers",
                        "order": 3,
                        "description": "Specialize in Kubernetes and Containerization, designing and managing production application orchestration. Integrate basic MLOps for supporting AI services.",
                        "education": [],
                        "skills": ["MLOps & Model Deployment"],
                        "certifications": [],
                        "specializations": ["Kubernetes and Containerization"],
                    },
                    {
                        "name": "Phase 4: SRE/Platform Lead",
                        "order": 4,
                        "description": "Move into a Site Reliability Engineer (SRE) or Platform Engineering Manager role, focusing on system observability and architectural governance.",
                        "education": [],
                        "skills": [],
                        "certifications": [],
                        "specializations": [],
                    }
                ]
            },

            # --- 7. NEW CAREER: UX/UI DESIGNER ---
            "UX/UI Designer": {
                "overview": "Focuses on user-centered design, creating accessible, efficient, and aesthetically pleasing digital interfaces.",
                "salary": 1150000.00,
                "outlook": "Strong and steady growth as digital products prioritize user experience.",
                "intro": {
                    "content": "A UX/UI Designer ensures that a product is both easy to use (UX - User Experience) and visually appealing (UI - User Interface). This role requires empathy, creativity, and a strong understanding of Human-Computer Interaction principles.",
                    "years": 4, "months": 0
                },
                "responsibilities": [
                    "Conducting user research, interviews, and usability testing to gather requirements.",
                    "Creating user flows, wireframes, and low-fidelity prototypes.",
                    "Designing high-fidelity user interfaces and ensuring visual consistency.",
                    "Developing and maintaining a standardized design system (components, styles).",
                    "Collaborating with product managers and engineers to ensure technical feasibility.",
                    "Iterating designs based on quantitative data (analytics) and qualitative feedback.",
                    "Ensuring digital products meet accessibility standards (WCAG).",
                    "Presenting design concepts and rationale to stakeholders.",
                    "Applying principles of Human-Computer Interaction (HCI) to solve design problems.",
                    "Staying current with design trends, tools, and best practices."
                ],
                "specializations": [
                    ("UX Researcher", "Focuses deeply on user testing, interviews, and data to inform design decisions."),
                    ("Design System Specialist", "Focuses on creating and maintaining the reusable components library and guidelines."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: Design Foundation",
                        "order": 1,
                        "description": "Complete a Bachelor of Design or HCI degree. Master core design principles, visual hierarchy, and basic tools like Figma/Sketch.",
                        "education": ["Bachelor of Design / HCI"],
                        "skills": ["Human-Computer Interaction (HCI)", "Wireframing & Prototyping", "User Research & Testing", "Project Management"],
                        "certifications": [],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: Prototyping & Testing",
                        "order": 2,
                        "description": "Build high-fidelity prototypes and conduct extensive user testing. Start collaborating closely with engineering teams.",
                        "education": [],
                        "skills": ["Data Visualization & BI", "Business Strategy & Market Analysis"],
                        "certifications": [],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 3: Design System Mastery",
                        "order": 3,
                        "description": "Contribute to or lead the creation of a reusable Design System. Focus on accessibility and cross-platform consistency. Deepen research skills.",
                        "education": [],
                        "skills": [],
                        "certifications": [],
                        "specializations": ["UX Researcher", "Design System Specialist"],
                    },
                    {
                        "name": "Phase 4: Leadership",
                        "order": 4,
                        "description": "Transition to a Head of Design or VP of Product Design role, setting the entire organization's design philosophy and user experience strategy.",
                        "education": [],
                        "skills": [],
                        "certifications": [],
                        "specializations": [],
                    }
                ]
            },

            # --- 8. NEW CAREER: NETWORK ENGINEER ---
            "Network Engineer": {
                "overview": "Designs, implements, and manages the network infrastructure that enables data transfer and connectivity across an organization.",
                "salary": 1200000.00,
                "outlook": "Steady and essential growth; crucial for cloud and hybrid IT environments.",
                "intro": {
                    "content": "Network Engineers are responsible for the availability and security of the organization’s digital plumbing. They deal with routers, switches, firewalls, and network topology, ensuring high performance and minimal downtime.",
                    "years": 4, "months": 0
                },
                "responsibilities": [
                    "Designing and configuring local area networks (LANs), wide area networks (WANs), and cloud networking (VPCs).",
                    "Installing and managing network hardware, including routers, switches, and load balancers.",
                    "Troubleshooting network connectivity, performance issues, and security incidents.",
                    "Implementing network security policies and firewall rules (Cybersecurity Fundamentals).",
                    "Monitoring network performance using specialized tools and optimizing traffic flow.",
                    "Maintaining detailed network documentation and topology diagrams.",
                    "Automating network tasks and infrastructure deployment using Python and scripting (CI/CD & Automation).",
                    "Managing network upgrades and migration projects.",
                    "Implementing disaster recovery and business continuity plans for network systems.",
                    "Collaborating with Cloud Architects on hybrid infrastructure solutions."
                ],
                "specializations": [
                    ("Cloud Networking Specialist", "Focuses on VPCs, gateways, and connectivity within AWS, Azure, or GCP."),
                    ("Data Center Engineer", "Focuses on high-density switching, fabric design, and physical infrastructure."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: Networking Base",
                        "order": 1,
                        "description": "Complete a Bachelor's degree. Obtain the CCNA certification and master core Networking & TCP/IP principles, IP addressing, and basic routing.",
                        "education": ["Bachelor of Computer Science"],
                        "skills": ["Networking & TCP/IP", "Linux Administration", "Cybersecurity Fundamentals"],
                        "certifications": ['Cisco Certified Network Associate (CCNA)'],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: Infrastructure Implementation",
                        "order": 2,
                        "description": "Gain hands-on experience with routing/switching implementation, firewall management, and SQL & Database Management for network device inventories.",
                        "education": ["BSc Cloud Computing / DevOps"],
                        "skills": ["SQL & Database Management", "Python Programming", "CI/CD & Automation"],
                        "certifications": [],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 3: Advanced Routing & Security",
                        "order": 3,
                        "description": "Focus on advanced security protocols, wide-area networking, and cloud networking (Cloud Architecture). Pursue professional-level certifications.",
                        "education": [],
                        "skills": ["Cloud Architecture", "System Architecture Design", "Risk Quantification"],
                        "certifications": [],
                        "specializations": ["Cloud Networking Specialist", "Data Center Engineer"],
                    },
                    {
                        "name": "Phase 4: Network Architect",
                        "order": 4,
                        "description": "Move into a Network Architect role, responsible for setting enterprise network strategy, high-level design, and security posture.",
                        "education": [],
                        "skills": [],
                        "certifications": [],
                        "specializations": [],
                    }
                ]
            },

            # --- 9. NEW CAREER: PRODUCT MANAGER (TECH) ---
            "Product Manager (Tech)": {
                "overview": "Defines the product vision, strategy, and roadmap, prioritizing features to maximize business value and meet customer needs.",
                "salary": 1650000.00,
                "outlook": "Extremely high value and growth; essential role linking business, technology, and users.",
                "intro": {
                    "content": "The Technical Product Manager is the 'CEO' of the product. This role requires a blend of technical understanding (to communicate with engineers) and business acumen (to understand the market and drive ROI). They are responsible for the 'what' and 'why' of the product.",
                    "years": 6, "months": 0
                },
                "responsibilities": [
                    "Defining the product vision, strategy, and long-term roadmap (Business Strategy & Market Analysis).",
                    "Gathering and prioritizing user requirements from research, data, and stakeholders.",
                    "Creating detailed user stories and managing the product backlog.",
                    "Leading Agile ceremonies (sprint planning, backlog grooming, retrospectives).",
                    "Communicating the product's value proposition to sales and marketing teams.",
                    "Monitoring key product metrics (KPIs) and using Data Visualization & BI to track performance.",
                    "Collaborating closely with engineering leads on technical feasibility and trade-offs.",
                    "Conducting competitive analysis and market research.",
                    "Managing product release cycles and go-to-market strategies.",
                    "Acting as the voice of the customer within the organization."
                ],
                "specializations": [
                    ("Growth PM", "Focuses on acquisition, activation, and retention metrics using A/B testing and rapid iteration."),
                    ("Technical PM (TPM)", "Focuses on platform, API, or infrastructure products, requiring deeper technical knowledge."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: Technical Base",
                        "order": 1,
                        "description": "Start with a technical background (e.g., Software Engineer or Data Analyst). Develop strong Project Management and communication skills.",
                        "education": ["Bachelor of Computer Science"],
                        "skills": ["Project Management", "Data Visualization & BI", "System Architecture Design", "Business Strategy & Market Analysis"],
                        "certifications": ['Certified Scrum Product Owner (CSPO)'],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: Product Associate Role",
                        "order": 2,
                        "description": "Work as an Associate PM or Scrum Master. Master backlog management, user story creation, and stakeholder management.",
                        "education": ["Master of Business Administration (MBA)"],
                        "skills": ["User Research & Testing", "SQL & Database Management", "CI/CD & Automation"],
                        "certifications": [],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 3: Product Leader (Group PM)",
                        "order": 3,
                        "description": "Manage a portfolio of products, specializing in a functional area (Growth or Technical). Deepen understanding of finance and market analysis (MBA completion).",
                        "education": [],
                        "skills": ["Risk Quantification", "Cloud Architecture"],
                        "certifications": [],
                        "specializations": ["Growth PM", "Technical PM (TPM)"],
                    },
                    {
                        "name": "Phase 4: C-Suite/VP Level",
                        "order": 4,
                        "description": "Lead the entire Product organization (Chief Product Officer or VP of Product), responsible for the company's entire product vision and financial success.",
                        "education": [],
                        "skills": [],
                        "certifications": [],
                        "specializations": [],
                    }
                ]
            },
        }


        # Ensure all operations within this block are treated as a single transaction
        with transaction.atomic():
            for career_name, data in career_data.items():
                self.stdout.write(self.style.NOTICE(f'\nProcessing Career: {career_name}'))

                # 3.1. Create the Career object
                career, created = Career.objects.get_or_create(
                    name=career_name,
                    defaults={
                        "sector": it_sector,
                        "overview": data["overview"],
                        "average_salary": Decimal(str(data["salary"])),
                        "job_outlook": data["outlook"],
                    }
                )
                self.stdout.write(self.style.SUCCESS(f'   Career {"created" if created else "retrieved"}.'))

                # 3.2. Create Introduction
                Introduction.objects.get_or_create(
                    career=career,
                    defaults={
                        "content": data["intro"]["content"],
                        "education_duration_years": data["intro"]["years"],
                        "education_duration_months": data["intro"]["months"],
                    }
                )

                # 3.3. Create Responsibilities (Delete existing first to prevent duplicates)
                Responsibility.objects.filter(career=career).delete()
                responsibilities = [
                    Responsibility(career=career, description=desc) 
                    for desc in data["responsibilities"]
                ]
                Responsibility.objects.bulk_create(responsibilities)

                # 3.4. Create Specializations
                current_specializations = {}
                for spec_name, spec_desc in data["specializations"]:
                    spec, _ = Specialization.objects.get_or_create(
                        career=career,
                        name=spec_name,
                        defaults={"description": spec_desc}
                    )
                    current_specializations[spec_name] = spec


                # 3.5. Create Roadmap (or retrieve existing)
                roadmap, _ = Roadmap.objects.get_or_create(
                    career=career,
                    defaults={"description": f"A comprehensive roadmap for becoming a top-tier {career_name}."}
                )
                
                # 3.6. Create Phases and link M2M relationships (The core of the request)
                # Delete existing phases to allow re-running the script
                Phase.objects.filter(roadmap=roadmap).delete()
                
                for phase_data in data["roadmap_phases"]:
                    phase = Phase.objects.create(
                        roadmap=roadmap,
                        name=phase_data["name"],
                        order=phase_data["order"],
                        description=phase_data["description"]
                    )
                    
                    # Link Education (M2M)
                    edu_objects = [education_map[name] for name in phase_data["education"] if name in education_map]
                    phase.required_education.add(*edu_objects)
                    
                    # Link Skills (M2M)
                    skill_objects = [skills_map[name] for name in phase_data["skills"] if name in skills_map]
                    phase.required_skills.add(*skill_objects)

                    # Link Certifications (M2M)
                    cert_objects = [cert_map[name] for name in phase_data["certifications"] if name in cert_map]
                    phase.required_certifications.add(*cert_objects)

                    # Link Specializations (M2M) - requires getting the Spec instance linked to the current Career
                    spec_objects = []
                    for spec_name in phase_data["specializations"]:
                        if spec_name in current_specializations:
                            spec_objects.append(current_specializations[spec_name])
                        else:
                             self.stdout.write(self.style.WARNING(f"Warning: Specialization '{spec_name}' not found for {career_name}. Check the specializations list."))

                    phase.required_specializations.add(*spec_objects)
                    
                    self.stdout.write(self.style.SUCCESS(f'      - Created Phase {phase.order}: {phase.name}'))

        self.stdout.write(self.style.SUCCESS('\nIT data population complete! 9 careers successfully defined.'))
        
