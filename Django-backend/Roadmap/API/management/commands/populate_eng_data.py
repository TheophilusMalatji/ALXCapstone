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
    help = 'Populates the database with detailed Engineering career data, localized for South Africa (ZAR, ECSA).'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting South African Engineering career data population...'))

        # --- 1. PRE-POPULATE LOOKUP DATA (Skills, Education, Certs) ---
        
        self.stdout.write(self.style.NOTICE('1. Creating global and SA-specific Skills, Education, and Certifications...'))

        # Create all unique skills needed across all Engineering careers
        skills_data = [
            # Core Engineering Skills (SA Context)
            ('ECSA Regulatory Compliance (Pr. Eng. Requirements)', 'Adherence to the Engineering Council of South Africa guidelines and continuous professional development.'),
            ('EPCM and Project Management (Local Large Projects)', 'Executing Engineering, Procurement, and Construction Management, crucial for infrastructure development.'),
            ('FEA and CFD Modeling (Advanced Simulation)', 'Finite Element Analysis and Computational Fluid Dynamics for structural integrity and flow dynamics.'),
            ('Water Resource Management (Local Scarcity/Infrastructure)', 'Designing solutions for water supply, purification, and wastewater treatment, addressing local shortages.'),
            ('Geotechnical Analysis & Ground Stability', 'Assessing soil and rock mechanics, essential for foundation design and mining operations.'),
            ('Mine Health and Safety Act (MHSA) Compliance', 'Mandatory regulatory knowledge for anyone working in or near a South African mining environment.'),
            ('Renewable Energy Systems (Solar/Wind Integration)', 'Designing and implementing grid-tied or off-grid solar and wind power solutions.'),
            ('High Voltage Power Distribution (Eskom/Transmission)', 'Designing, operating, and maintaining electrical grid infrastructure up to 400kV and beyond.'),
            # Core Tech/Cross-Sector Skills (Since user mentioned software)
            ('Advanced Data Structures & Algorithms', 'Designing efficient software systems and logic, core to Software Engineering.'),
            ('Cybersecurity for OT/IT (Operational Technology)', 'Securing industrial control systems, SCADA, and IoT devices in critical infrastructure.'),
            ('Agile and DevOps Methodologies', 'Accelerating product delivery through automation and iterative development processes.')
        ]
        skills_map = {name: Skill.objects.get_or_create(name=name, description=desc)[0] for name, desc in skills_data}
        self.stdout.write(self.style.SUCCESS(f'   Created {len(skills_map)} skills.'))

        # Create all unique education options
        education_data = [
            ('BEng / BSc Engineering (ECSA Accredited)', 'Four-year degree required for the Professional Engineer (Pr. Eng.) path.', 8, 4.0),
            ('BTech Engineering (ECSA Technologist Path)', 'Degree often pursued by technologists, leading to the Professional Engineering Technologist (Pr. Tech. Eng.) path.', 7, 4.0),
            ('MSc / MEng Engineering (Specialist Focus)', 'Advanced degree providing specialized knowledge in areas like structural, power, or software engineering.', 9, 2.0),
            ('Master of Business Administration (MBA) - Technical Leadership', 'Advanced management degree focused on leading technical organizations and strategy.', 9, 2.0),
        ]
        education_map = {name: Education.objects.get_or_create(name=name, description=desc, nqf_level=nqf, duration_years=Decimal(duration))[0] 
                         for name, desc, nqf, duration in education_data}
        self.stdout.write(self.style.SUCCESS(f'   Created {len(education_map)} education options.'))

        # Create certifications (SA-focused)
        certifications_data = [
            ('Pr. Eng. (Professional Engineer - ECSA)', 'The mandatory professional registration for full accountability of complex engineering work in South Africa.', 'ECSA'),
            ('Pr. Tech. Eng. (Professional Engineering Technologist - ECSA)', 'Professional registration for complex technological tasks and project management.', 'ECSA'),
            ('PMP (Project Management Professional)', 'Globally recognized certification for leading and directing projects across industries.', 'PMI/Global'),
            ('Cert. in Mine Health and Safety (CMHS)', 'A critical local certification for engineers assuming managerial roles in the mining sector.', 'SA Regulator'),
            ('AWS or Azure Cloud Certification', 'Certification proving expertise in cloud infrastructure and scalable application deployment.', 'Global Tech Provider'),
        ]
        cert_map = {name: Certification.objects.get_or_create(name=name, description=desc)[0] 
                    for name, desc, body in certifications_data}
        self.stdout.write(self.style.SUCCESS(f'   Created {len(cert_map)} certifications.'))


        # --- 2. CREATE SECTOR ---
        engineering_sector, _ = Sector.objects.get_or_create(
            name="Engineering",
            defaults={
                "description": "The application of scientific principles to design, build, and maintain structures, machines, and systems, with a strong emphasis on ECSA professional standards and South African infrastructure needs."
            }
        )
        self.stdout.write(self.style.SUCCESS('2. Created Sector: Engineering.'))


        # --- 3. CAREER DATA DEFINITION & POPULATION ---

        career_data = {
            # --- 1. CIVIL ENGINEER ---
            "Civil Engineer": {
                "overview": "Designs, constructs, and maintains physical and naturally built environments, including roads, bridges, dams, and water systems critical to South African infrastructure.",
                "salary": 900000.00, # ZAR Annual (Mid-Senior Pr. Eng.)
                "outlook": "Strong and stable, driven by ongoing governmental infrastructure spending (pr. roads, water) and urbanization projects.",
                "intro": {
                    "content": "The Civil Engineer is responsible for the foundations of society. This role requires mastery of Geotechnical Analysis and EPCM and Project Management. In South Africa, a key focus is Water Resource Management due to scarcity and maintaining infrastructure against environmental factors. Professional registration as a **Pr. Eng. (ECSA)** is the standard of practice.",
                    "years": 7, "months": 0
                },
                "responsibilities": [
                    "Designing infrastructure projects (roads, buildings, water treatment plants) using specialized software.",
                    "Conducting site investigations and Geotechnical Analysis & Ground Stability studies.",
                    "Managing project timelines, budgets, and procurement using EPCM and Project Management (Local Large Projects).",
                    "Ensuring all designs adhere to local building codes, SABS standards, and ECSA Regulatory Compliance (Pr. Eng. Requirements).",
                    "Developing plans for Water Resource Management (Local Scarcity/Infrastructure) and sanitation.",
                    "Overseeing construction activities and conducting quality assurance inspections.",
                    "Performing FEA and CFD Modeling (Advanced Simulation) for complex structural designs.",
                    "Preparing tender documents and evaluating contractor proposals."
                ],
                "specializations": [
                    ("Structural Engineer", "Specializing in the design and load-bearing integrity of buildings, bridges, and tunnels."),
                    ("Water Engineer", "Focusing on hydrology, hydraulics, and municipal water supply systems."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: Academic Foundation & Candidate Phase",
                        "order": 1,
                        "description": "Complete BEng/BSc Engineering (ECSA Accredited). Register as a Candidate Engineer with ECSA and begin structured training (typically 3 years).",
                        "education": ["BEng / BSc Engineering (ECSA Accredited)"],
                        "skills": ["FEA and CFD Modeling (Advanced Simulation)", "Geotechnical Analysis & Ground Stability"],
                        "certifications": [],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: Professional Registration (Pr. Eng.)",
                        "order": 2,
                        "description": "Achieve Professional Engineer (Pr. Eng.) registration after meeting ECSA competency requirements. Start managing smaller projects independently.",
                        "education": [],
                        "skills": ["ECSA Regulatory Compliance (Pr. Eng. Requirements)", "EPCM and Project Management (Local Large Projects)", "Water Resource Management (Local Scarcity/Infrastructure)"],
                        "certifications": ["Pr. Eng. (Professional Engineer - ECSA)"],
                        "specializations": ["Structural Engineer"],
                    },
                    {
                        "name": "Phase 3: Senior Project Manager",
                        "order": 3,
                        "description": "Lead multi-disciplinary teams on large infrastructure projects. Obtain PMP certification for advanced project governance.",
                        "education": ["MSc / MEng Engineering (Specialist Focus)"],
                        "skills": [],
                        "certifications": ["PMP (Project Management Professional)"],
                        "specializations": ["Water Engineer"],
                    },
                    {
                        "name": "Phase 4: Technical Director/Principal Engineer",
                        "order": 4,
                        "description": "Assume executive oversight for the engineering department, focusing on strategic bids and public-private partnerships. MBA highly beneficial for leadership.",
                        "education": ["Master of Business Administration (MBA) - Technical Leadership"],
                        "skills": [],
                        "certifications": [],
                        "specializations": [],
                    }
                ]
            },
            
            # --- 2. ELECTRICAL ENGINEER ---
            "Electrical Engineer": {
                "overview": "Designs and manages power systems, electrical machines, and high-voltage transmission/distribution networks, with a vital role in South Africa's energy sector (Eskom and Renewables).",
                "salary": 1100000.00, # ZAR Annual (Specialist/Eskom/Private Power)
                "outlook": "Exceptional growth, especially in Renewable Energy Systems, battery storage, and smart grid technology due to the energy crisis.",
                "intro": {
                    "content": "The Electrical Engineer powers the economy. Success requires expertise in High Voltage Power Distribution and Renewable Energy Systems. They are integral to both utility-scale projects (Eskom/IPPs) and industrial power systems, ensuring rigorous ECSA standards are met. Many follow the **Pr. Tech. Eng.** path via a BTech degree.",
                    "years": 6, "months": 0
                },
                "responsibilities": [
                    "Designing high-voltage (HV) transmission and distribution substations.",
                    "Integrating Renewable Energy Systems (Solar/Wind Integration) into the national grid.",
                    "Performing load flow analysis and short-circuit studies.",
                    "Ensuring designs meet ECSA Regulatory Compliance (Pr. Eng. Requirements) and local safety standards.",
                    "Managing large-scale power projects using EPCM and Project Management (Local Large Projects).",
                    "Implementing Cybersecurity for OT/IT (Operational Technology) in SCADA and control systems.",
                    "Conducting maintenance and fault analysis on High Voltage Power Distribution (Eskom/Transmission) equipment.",
                    "Developing specifications for electrical equipment and managing procurement."
                ],
                "specializations": [
                    ("High Voltage Specialist", "Focusing on transmission, protection relay systems, and substations."),
                    ("Renewables Engineer", "Specializing in utility-scale solar farms, wind parks, and grid code compliance."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: Academic & Candidate Technologist",
                        "order": 1,
                        "description": "Complete BEng/BTech Engineering. Register as a Candidate Engineer/Technologist and begin the ECSA training program.",
                        "education": ["BEng / BSc Engineering (ECSA Accredited)", "BTech Engineering (ECSA Technologist Path)"],
                        "skills": ["Renewable Energy Systems (Solar/Wind Integration)", "High Voltage Power Distribution (Eskom/Transmission)"],
                        "certifications": [],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: Professional Registration (Pr. Eng. / Pr. Tech. Eng.)",
                        "order": 2,
                        "description": "Achieve Pr. Eng. or Pr. Tech. Eng. registration. Start specializing in either power systems or electronics and embedded systems.",
                        "education": [],
                        "skills": ["ECSA Regulatory Compliance (Pr. Eng. Requirements)", "EPCM and Project Management (Local Large Projects)", "Cybersecurity for OT/IT (Operational Technology)"],
                        "certifications": ["Pr. Eng. (Professional Engineer - ECSA)", "Pr. Tech. Eng. (Professional Engineering Technologist - ECSA)"],
                        "specializations": ["Renewables Engineer"],
                    },
                    {
                        "name": "Phase 3: Senior Technical Specialist",
                        "order": 3,
                        "description": "Lead technical design teams for major projects. Complete an MSc or specialized qualification in power electronics or energy systems.",
                        "education": ["MSc / MEng Engineering (Specialist Focus)"],
                        "skills": ["FEA and CFD Modeling (Advanced Simulation)"],
                        "certifications": [],
                        "specializations": ["High Voltage Specialist"],
                    },
                    {
                        "name": "Phase 4: Engineering Manager / Consultant",
                        "order": 4,
                        "description": "Transition to a leadership role in an energy utility, consulting firm, or large industrial plant. MBA or advanced technical management training is key.",
                        "education": ["Master of Business Administration (MBA) - Technical Leadership"],
                        "skills": [],
                        "certifications": [],
                        "specializations": [],
                    }
                ]
            },

            # --- 3. MINING ENGINEER ---
            "Mining Engineer": {
                "overview": "Designs, plans, and manages the extraction of valuable minerals from the earth (e.g., gold, platinum, coal, iron ore), focusing on safety and economic feasibility.",
                "salary": 1300000.00, # ZAR Annual (Highly Compensated due to risk/demand)
                "outlook": "Essential South African role, highly dependent on global commodity cycles but with consistent domestic demand for experienced and compliant leaders.",
                "intro": {
                    "content": "Mining Engineers operate at the heart of South Africa’s oldest industry. The job is highly regulated, requiring absolute mastery of the **Mine Health and Safety Act (MHSA) Compliance** and Geotechnical Analysis. Progression to managerial roles requires not just technical skill, but also certified managerial qualifications.",
                    "years": 7, "months": 0
                },
                "responsibilities": [
                    "Designing mine layouts, tunnels, and open-pit geometries.",
                    "Planning and scheduling extraction operations to maximize yield and safety.",
                    "Ensuring strict Mine Health and Safety Act (MHSA) Compliance in all operations.",
                    "Conducting Geotechnical Analysis & Ground Stability assessments to prevent collapses.",
                    "Managing budgets and resources using EPCM and Project Management (Local Large Projects).",
                    "Utilizing simulation tools for ventilation, rock mechanics, and resource modeling.",
                    "Overseeing and optimizing drilling, blasting, and material handling processes.",
                    "Collaborating with metallurgists and geologists.",
                    "Ensuring adherence to ECSA Regulatory Compliance (Pr. Eng. Requirements).",
                    "Implementing Water Resource Management solutions for mine dewatering and processing."
                ],
                "specializations": [
                    ("Rock Mechanics Engineer", "Specializing in the mechanical behavior of rock masses, crucial for deep-level mining safety."),
                    ("Mine Planner", "Focusing on long-term economic and operational optimization of the mine life cycle."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: Academic & Candidate Engineer",
                        "order": 1,
                        "description": "Complete BEng/BSc Engineering (Mining). Register as a Candidate Engineer with ECSA and enter the mandatory underground/operational training phase.",
                        "education": ["BEng / BSc Engineering (ECSA Accredited)"],
                        "skills": ["Geotechnical Analysis & Ground Stability", "Mine Health and Safety Act (MHSA) Compliance"],
                        "certifications": [],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: Professional Registration & CMHS",
                        "order": 2,
                        "description": "Achieve Pr. Eng. status. Secure the mandatory Cert. in Mine Health and Safety (CMHS) to qualify for senior operational roles.",
                        "education": [],
                        "skills": ["ECSA Regulatory Compliance (Pr. Eng. Requirements)", "EPCM and Project Management (Local Large Projects)", "FEA and CFD Modeling (Advanced Simulation)"],
                        "certifications": ["Pr. Eng. (Professional Engineer - ECSA)", "Cert. in Mine Health and Safety (CMHS)"],
                        "specializations": ["Rock Mechanics Engineer"],
                    },
                    {
                        "name": "Phase 3: Mine Manager / Senior Leader",
                        "order": 3,
                        "description": "Take on a statutory manager role, responsible for the entire mine section's safety and production. PMP certification is useful for complex capital projects.",
                        "education": ["MSc / MEng Engineering (Specialist Focus)"],
                        "skills": ["Water Resource Management (Local Scarcity/Infrastructure)"],
                        "certifications": ["PMP (Project Management Professional)"],
                        "specializations": ["Mine Planner"],
                    },
                    {
                        "name": "Phase 4: Technical Executive / CEO",
                        "order": 4,
                        "description": "Executive level role overseeing multiple mines or the group's technical strategy. Requires significant business acumen and leadership training.",
                        "education": ["Master of Business Administration (MBA) - Technical Leadership"],
                        "skills": [],
                        "certifications": [],
                        "specializations": [],
                    }
                ]
            },

            # --- 4. SOFTWARE ENGINEER (SA/FinTech Focus) ---
            "Software Engineer": {
                "overview": "Designs, develops, and maintains scalable software applications and systems, particularly within the fast-growing South African financial (FinTech) and enterprise sectors.",
                "salary": 1050000.00, # ZAR Annual (Senior/Specialist)
                "outlook": "Exponential growth, high demand for cloud and distributed systems expertise across all major South African cities.",
                "intro": {
                    "content": "Software Engineers are the architects of the digital world. The role demands mastery of **Advanced Data Structures & Algorithms** and Agile methodologies. Crucially, they must integrate **Cybersecurity for OT/IT** and cloud best practices to build secure, high-performance systems for local banks and businesses. While ECSA is rare, the **Pr. Eng.** designation is possible for those focused on safety-critical systems.",
                    "years": 5, "months": 0
                },
                "responsibilities": [
                    "Designing system architecture and coding high-performance software modules.",
                    "Implementing solutions using Advanced Data Structures & Algorithms.",
                    "Applying Agile and DevOps Methodologies (CI/CD pipelines, automated testing).",
                    "Ensuring system security and regulatory compliance via Cybersecurity for OT/IT (Operational Technology).",
                    "Collaborating with product managers and business analysts (often finance-focused).",
                    "Optimizing database performance and managing data integrity.",
                    "Mentoring junior developers and performing code reviews.",
                    "Developing robust API integrations for third-party systems.",
                    "Managing cloud infrastructure and deployment (AWS/Azure).",
                    "Conducting continuous integration and continuous deployment (CI/CD) activities."
                ],
                "specializations": [
                    ("DevOps Engineer", "Specializing in automation, infrastructure as code, and continuous delivery pipelines."),
                    ("Solutions Architect", "Designing the overall structure and technology stack for large, complex enterprise systems."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: Academic & Junior Developer",
                        "order": 1,
                        "description": "Complete BEng/BSc Engineering or BSc Computer Science. Secure a junior developer role. Focus on core programming and Advanced Data Structures & Algorithms.",
                        "education": ["BEng / BSc Engineering (ECSA Accredited)"],
                        "skills": ["Advanced Data Structures & Algorithms", "Agile and DevOps Methodologies"],
                        "certifications": [],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: Senior Developer & Cloud Expertise",
                        "order": 2,
                        "description": "Advance to Senior Developer, leading major features. Obtain AWS or Azure Cloud Certification and specialize in a platform or language.",
                        "education": ["BTech Engineering (ECSA Technologist Path)"],
                        "skills": ["Cybersecurity for OT/IT (Operational Technology)", "EPCM and Project Management (Local Large Projects)"],
                        "certifications": ["AWS or Azure Cloud Certification"],
                        "specializations": ["DevOps Engineer"],
                    },
                    {
                        "name": "Phase 3: Technical Lead/Architect",
                        "order": 3,
                        "description": "Lead the technical direction for multiple projects. Formalize leadership with ECSA registration (if applicable) or a PMP.",
                        "education": ["MSc / MEng Engineering (Specialist Focus)"],
                        "skills": ["ECSA Regulatory Compliance (Pr. Eng. Requirements)", "FEA and CFD Modeling (Advanced Simulation)"],
                        "certifications": ["Pr. Eng. (Professional Engineer - ECSA)", "PMP (Project Management Professional)"],
                        "specializations": ["Solutions Architect"],
                    },
                    {
                        "name": "Phase 4: Chief Technology Officer (CTO)",
                        "order": 4,
                        "description": "Executive role driving the company's long-term technology strategy, product innovation, and enterprise security. MBA is highly relevant.",
                        "education": ["Master of Business Administration (MBA) - Technical Leadership"],
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
                        "sector": engineering_sector,
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
                # Delete existing specializations for this career to ensure clean update
                Specialization.objects.filter(career=career).delete() 
                for spec_name, spec_desc in data["specializations"]:
                    spec, _ = Specialization.objects.get_or_create(
                        career=career,
                        name=spec_name,
                        defaults={"description": spec_desc}
                    )
                    current_specializations[spec_name] = spec


                # 3.5. Create Roadmap (Note: using 'description' field as requested)
                roadmap, _ = Roadmap.objects.get_or_create(
                    career=career,
                    defaults={"description": f"A structured progression through academic qualifications, practical experience, and ECSA registration to become a professionally registered {career_name} in South Africa."}
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

        self.stdout.write(self.style.SUCCESS('\nSouth African Engineering data population complete! 4 core careers successfully defined (ZAR, ECSA integrated).'))