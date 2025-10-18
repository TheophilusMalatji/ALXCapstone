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
    help = 'Populates the database with detailed Healthcare/Nursing career data (9 roles).'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting Nursing career data population...'))

        # --- 1. PRE-POPULATE LOOKUP DATA (Skills, Education, Certs) ---
        
        self.stdout.write(self.style.NOTICE('1. Creating global Skills, Education, and Certifications...'))

        # Create all unique skills needed across all Nursing careers
        skills_data = [
            # Core Clinical Skills
            ('Clinical Assessment', 'Performing thorough physical and psychosocial assessments of patients.'),
            ('Pharmacology & Medication Administration', 'Safe and accurate knowledge of drug effects, dosages, and administration routes.'),
            ('Critical Thinking & Prioritization', 'Ability to analyze complex patient situations and prioritize interventions under pressure.'),
            ('Infection Control & Sterilization', 'Strict adherence to protocols to prevent and control the spread of infectious diseases.'),
            ('Trauma & Emergency Response (ACLS/BLS)', 'Proficiency in advanced and basic life support measures during medical emergencies.'),
            # Specialized Skills
            ('Advanced Pathophysiology', 'Deep understanding of disease processes at the cellular and systemic level (required for NP/CRNA).'),
            ('Patient Education & Advocacy', 'Teaching patients about their condition and advocating for their best interests.'),
            ('Electronic Medical Records (EMR) Management', 'Expertise in charting, data entry, and utilizing hospital information systems.'),
            ('Epidemiology & Biostatistics', 'Study of disease patterns and application of statistical methods in population health.'),
            ('Informatics & Data Security', 'Managing large healthcare datasets and ensuring compliance with HIPAA/HITECH.'),
            ('Surgical/Anesthesia Monitoring', 'Specialized monitoring of physiological responses during surgical procedures.'),
        ]
        skills_map = {name: Skill.objects.get_or_create(name=name, description=desc)[0] for name, desc in skills_data}
        self.stdout.write(self.style.SUCCESS(f'   Created {len(skills_map)} skills.'))

        # Create all unique education options
        education_data = [
            ('Associate Degree in Nursing (ADN)', 'Basic clinical training, often used as a stepping stone to a BSN.', 6, 2.0),
            ('Bachelor of Science in Nursing (BSN)', 'Standard entry-level education, including clinical practice and liberal arts.', 7, 4.0),
            ('Master of Science in Nursing (MSN)', 'Required for advanced practice roles (NP, CRNA) and administration.', 9, 2.0),
            ('Doctor of Nursing Practice (DNP)', 'Terminal degree for clinical practice, leadership, and policy development.', 10, 3.0),
        ]
        education_map = {name: Education.objects.get_or_create(name=name, description=desc, nqf_level=nqf, duration_years=Decimal(duration))[0] 
                         for name, desc, nqf, duration in education_data}
        self.stdout.write(self.style.SUCCESS(f'   Created {len(education_map)} education options.'))

        # Create certifications (simple model)
        certifications_data = [
            ('NCLEX-RN', 'National Council Licensure Examination for Registered Nurses (required for initial licensure).'),
            ('CCRN', 'Certification for Adult Critical Care Nurses (highly valued in ICU/ER).'),
            ('CEN', 'Certified Emergency Nurse (specialized certification for ER).'),
            ('ANCC Board Certification (NP)', 'Certifies advanced knowledge in a specific population (e.g., Family NP, Acute Care NP).'),
            ('CRNA Certification', 'Certification required to practice as a Certified Registered Nurse Anesthetist.'),
            ('CPHIMS', 'Certified Professional in Health Information and Management Systems (for Informatics).'),
        ]
        cert_map = {name: Certification.objects.get_or_create(name=name, description=desc)[0] for name, desc in certifications_data}
        self.stdout.write(self.style.SUCCESS(f'   Created {len(cert_map)} certifications.'))


        # --- 2. CREATE SECTOR ---
        nursing_sector, _ = Sector.objects.get_or_create(
            name="Healthcare/Nursing",
            defaults={
                "description": "Clinical and administrative roles focused on direct patient care, health promotion, disease management, and advanced practice."
            }
        )
        self.stdout.write(self.style.SUCCESS('2. Created Sector: Healthcare/Nursing.'))


        # --- 3. CAREER DATA DEFINITION & POPULATION ---

        career_data = {
            # --- 1. CORE ROLE: REGISTERED NURSE (RN) ---
            "Registered Nurse (RN)": {
                "overview": "Provides and coordinates patient care, educates patients and the public about health conditions, and provides emotional support.",
                "salary": 750000.00,
                "outlook": "Excellent growth driven by aging populations and complex chronic diseases.",
                "intro": {
                    "content": "The RN is the frontline coordinator of patient care. This role demands strong Clinical Assessment skills, critical thinking, and a deep knowledge of Pharmacology. RNs are responsible for initial assessments, administering treatments, and communicating with the entire care team.",
                    "years": 4, "months": 0
                },
                "responsibilities": [
                    "Performing initial and ongoing Clinical Assessment of patient health status.",
                    "Administering medications and treatments as prescribed, utilizing Pharmacology & Medication Administration knowledge.",
                    "Collaborating with physicians and other healthcare professionals to develop and manage care plans.",
                    "Providing patient and family education on disease management, discharge planning, and self-care.",
                    "Documenting all patient care, observations, and interventions accurately in the Electronic Medical Records (EMR) Management system.",
                    "Ensuring adherence to Infection Control & Sterilization protocols.",
                    "Responding rapidly to changes in patient condition and initiating Trauma & Emergency Response (ACLS/BLS).",
                    "Acting as a Patient Education & Advocacy liaison between the patient and the healthcare system.",
                    "Supervising Licensed Practical Nurses (LPNs) and nursing aides.",
                    "Participating in quality improvement initiatives based on Evidence-Based Practice (EBP)."
                ],
                "specializations": [
                    ("Med-Surg RN", "General patient care across various medical conditions and surgical recovery."),
                    ("Telemetry RN", "Specializing in monitoring and interpreting cardiac rhythms."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: Licensure & Competency",
                        "order": 1,
                        "description": "Complete BSN, pass the NCLEX-RN, and master core clinical skills in an entry-level nursing position.",
                        "education": ["Bachelor of Science in Nursing (BSN)"],
                        "skills": ["Clinical Assessment", "Pharmacology & Medication Administration", "Critical Thinking & Prioritization", "Infection Control & Sterilization"],
                        "certifications": ["NCLEX-RN"],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: Specialty Development",
                        "order": 2,
                        "description": "Gain experience in a specialized unit (e.g., ICU, ER). Obtain BLS/ACLS certification and demonstrate proficiency in Trauma & Emergency Response.",
                        "education": ["Associate Degree in Nursing (ADN)"], # Often done as a bridge program
                        "skills": ["Trauma & Emergency Response (ACLS/BLS)", "Electronic Medical Records (EMR) Management", "Patient Education & Advocacy"],
                        "certifications": [],
                        "specializations": ["Med-Surg RN", "Telemetry RN"],
                    },
                    {
                        "name": "Phase 3: Charge Nurse/Preceptor",
                        "order": 3,
                        "description": "Take on formal leadership roles such as Charge Nurse or Preceptor, mentoring new staff and managing unit operations.",
                        "education": [],
                        "skills": ["Advanced Pathophysiology", "Epidemiology & Biostatistics"],
                        "certifications": [],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 4: Management/Advanced Practice Track",
                        "order": 4,
                        "description": "Transition to a Nursing Manager role (with MSN) or pursue an Advanced Practice track (NP/CRNA) via the MSN/DNP pathway.",
                        "education": ["Master of Science in Nursing (MSN)"],
                        "skills": [],
                        "certifications": [],
                        "specializations": [],
                    }
                ]
            },
            
            # --- 2. ADVANCED ROLE: NURSE PRACTITIONER (NP) ---
            "Nurse Practitioner (NP)": {
                "overview": "An Advanced Practice Registered Nurse (APRN) who can diagnose illnesses, manage treatment plans, and prescribe medications autonomously.",
                "salary": 1250000.00,
                "outlook": "Explosive growth due to physician shortages and expanded scope of practice.",
                "intro": {
                    "content": "Nurse Practitioners provide comprehensive, often primary, care. They require extensive clinical experience and a graduate degree (MSN or DNP) to achieve the depth of knowledge needed for diagnosis and prescription. They blend advanced medical knowledge with a holistic nursing approach.",
                    "years": 6, "months": 0
                },
                "responsibilities": [
                    "Obtaining comprehensive patient histories and performing physical examinations.",
                    "Ordering, performing, and interpreting diagnostic tests (e.g., X-rays, lab work).",
                    "Diagnosing acute and chronic conditions and developing treatment plans.",
                    "Prescribing medications and other therapies within scope of practice.",
                    "Managing ongoing care for patients with chronic diseases (e.g., diabetes, hypertension).",
                    "Providing counseling and education to promote health and prevent disease.",
                    "Collaborating with physicians and specialists in complex cases.",
                    "Conducting minor in-office procedures.",
                    "Maintaining current board certification in a specialty population (e.g., Family, Pediatrics, Acute Care).",
                    "Utilizing Advanced Pathophysiology knowledge to understand disease progression."
                ],
                "specializations": [
                    ("Family Nurse Practitioner (FNP)", "Primary care for individuals across the lifespan."),
                    ("Acute Care Nurse Practitioner (ACNP)", "Focus on critically ill patients in inpatient settings (ICU, hospital wards)."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: RN Foundation",
                        "order": 1,
                        "description": "Obtain RN licensure (BSN), gain 2+ years of experience in a relevant clinical setting (e.g., med-surg, ICU).",
                        "education": ["Bachelor of Science in Nursing (BSN)"],
                        "skills": ["Clinical Assessment", "Pharmacology & Medication Administration", "Critical Thinking & Prioritization"],
                        "certifications": ["NCLEX-RN"],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: Graduate Study",
                        "order": 2,
                        "description": "Enroll in and complete an MSN or DNP program, focusing on a specific population (e.g., Family, Acute Care).",
                        "education": ["Master of Science in Nursing (MSN)"],
                        "skills": ["Advanced Pathophysiology", "Epidemiology & Biostatistics", "Patient Education & Advocacy"],
                        "certifications": [],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 3: Certification & Practice",
                        "order": 3,
                        "description": "Pass national board certification (ANCC) and begin practice. Focus on building an independent patient panel or working in a collaborative practice.",
                        "education": ["Doctor of Nursing Practice (DNP)"],
                        "skills": ["Trauma & Emergency Response (ACLS/BLS)"],
                        "certifications": ["ANCC Board Certification (NP)"],
                        "specializations": ["Family Nurse Practitioner (FNP)", "Acute Care Nurse Practitioner (ACNP)"],
                    },
                    {
                        "name": "Phase 4: Clinical Leadership",
                        "order": 4,
                        "description": "Lead advanced clinical programs, teach at the graduate level, or open an independent practice (where allowed by state law).",
                        "education": [],
                        "skills": [],
                        "certifications": [],
                        "specializations": [],
                    }
                ]
            },

            # --- 3. CRITICAL CARE NURSE (ICU/ER) ---
            "Critical Care Nurse (ICU/ER)": {
                "overview": "Cares for patients with life-threatening illnesses or injuries, requiring high vigilance and rapid, advanced intervention.",
                "salary": 850000.00,
                "outlook": "High demand in hospitals; positions require specialized training and high emotional resilience.",
                "intro": {
                    "content": "Critical Care Nurses are masters of emergency and advanced interventions. They utilize complex monitoring equipment, manage multiple life-support systems, and must deploy Trauma & Emergency Response protocols instantly.",
                    "years": 4, "months": 0
                },
                "responsibilities": [
                    "Continuously monitoring complex physiological parameters (hemodynamics, neurological status).",
                    "Managing patients on mechanical ventilation and continuous renal replacement therapy (CRRT).",
                    "Titrating high-risk medications (e.g., vasoactive drips) based on immediate patient response.",
                    "Rapidly assessing and intervening during patient deterioration (Trauma & Emergency Response).",
                    "Utilizing Clinical Assessment skills to detect subtle changes in unstable patients.",
                    "Collaborating closely with critical care physicians and respiratory therapists.",
                    "Providing intense emotional support and communication to families during crises.",
                    "Maintaining proficiency in advanced cardiac life support (ACLS).",
                    "Documenting minute-by-minute status updates in the EMR.",
                    "Adhering to strict Infection Control & Sterilization protocols in high-risk environments."
                ],
                "specializations": [
                    ("Surgical ICU Nurse", "Specializing in post-operative care for complex surgeries."),
                    ("Emergency Department Nurse (ED)", "Specializing in the initial assessment and stabilization of acutely ill or injured patients."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: Foundation & ACLS",
                        "order": 1,
                        "description": "Complete BSN, obtain RN license, and achieve ACLS certification. Gain 1-2 years experience in a high-acuity setting (Telemetry or Med-Surg).",
                        "education": ["Bachelor of Science in Nursing (BSN)"],
                        "skills": ["Clinical Assessment", "Pharmacology & Medication Administration", "Trauma & Emergency Response (ACLS/BLS)"],
                        "certifications": ["NCLEX-RN"],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: Critical Care Entry",
                        "order": 2,
                        "description": "Transfer to ICU or ER. Master hemodynamic monitoring and advanced life-support equipment. Demonstrate superior Critical Thinking & Prioritization.",
                        "education": [],
                        "skills": ["Critical Thinking & Prioritization", "Advanced Pathophysiology", "Infection Control & Sterilization"],
                        "certifications": [],
                        "specializations": ["Emergency Department Nurse (ED)"],
                    },
                    {
                        "name": "Phase 3: Certification & Expertise",
                        "order": 3,
                        "description": "Obtain CCRN (ICU) or CEN (ER) certification. Become a unit expert, training new staff and leading quality initiatives.",
                        "education": [],
                        "skills": ["Patient Education & Advocacy"],
                        "certifications": ["CCRN", "CEN"],
                        "specializations": ["Surgical ICU Nurse"],
                    },
                    {
                        "name": "Phase 4: Advanced Practice",
                        "order": 4,
                        "description": "Pursue Acute Care Nurse Practitioner (ACNP) or Clinical Nurse Specialist (CNS) role via MSN/DNP pathway.",
                        "education": ["Master of Science in Nursing (MSN)"],
                        "skills": [],
                        "certifications": [],
                        "specializations": [],
                    }
                ]
            },

            # --- 4. PUBLIC HEALTH NURSE ---
            "Public Health Nurse": {
                "overview": "Focuses on health promotion, disease prevention, and community education for populations rather than individuals.",
                "salary": 720000.00,
                "outlook": "Increasing focus on preventative care and health equity drives consistent demand.",
                "intro": {
                    "content": "Public Health Nurses are critical to population health. They analyze community health data using Epidemiology & Biostatistics, create vaccination programs, manage disease outbreaks, and advocate for policy change.",
                    "years": 4, "months": 0
                },
                "responsibilities": [
                    "Assessing the health needs and environmental factors affecting entire communities.",
                    "Developing and implementing public health education campaigns (e.g., nutrition, smoking cessation).",
                    "Conducting large-scale immunization clinics and screening programs.",
                    "Investigating and managing communicable disease outbreaks using Epidemiology & Biostatistics.",
                    "Lobbying for health-related policy changes at local and state levels (Patient Education & Advocacy).",
                    "Providing health counseling and referrals to vulnerable or underserved populations.",
                    "Collaborating with government agencies, schools, and community organizations.",
                    "Applying principles of Infection Control & Sterilization at the community level.",
                    "Utilizing Clinical Assessment skills in community clinic settings.",
                    "Managing records for public health surveillance programs."
                ],
                "specializations": [
                    ("School Nurse", "Manages student health, screenings, and communicable disease control in an educational setting."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: Clinical & Community Exposure",
                        "order": 1,
                        "description": "Complete BSN, obtain RN license. Gain initial clinical experience, preferably in an outpatient or community clinic.",
                        "education": ["Bachelor of Science in Nursing (BSN)"],
                        "skills": ["Clinical Assessment", "Patient Education & Advocacy", "Infection Control & Sterilization"],
                        "certifications": ["NCLEX-RN"],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: Population Health Skills",
                        "order": 2,
                        "description": "Master core public health competencies, including disease tracking, grant writing, and community organizing. Learn Epidemiology & Biostatistics.",
                        "education": [],
                        "skills": ["Epidemiology & Biostatistics", "Critical Thinking & Prioritization"],
                        "certifications": [],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 3: Program Leadership",
                        "order": 3,
                        "description": "Lead public health programs (e.g., WIC, immunizations). Pursue a Master of Public Health (MPH) or MSN for leadership roles.",
                        "education": ["Master of Science in Nursing (MSN)"],
                        "skills": ["Pharmacology & Medication Administration", "Electronic Medical Records (EMR) Management"],
                        "certifications": [],
                        "specializations": ["School Nurse"],
                    },
                    {
                        "name": "Phase 4: Policy & Director Level",
                        "order": 4,
                        "description": "Serve as a Health Department Director or Policy Advisor, driving state-level public health initiatives.",
                        "education": [],
                        "skills": [],
                        "certifications": [],
                        "specializations": [],
                    }
                ]
            },
            
            # --- 5. MENTAL HEALTH NURSE (Psychiatric) ---
            "Mental Health Nurse (Psychiatric)": {
                "overview": "Provides care, therapy, and crisis management for patients with mental illnesses or behavioral disorders.",
                "salary": 800000.00,
                "outlook": "Very high demand due to increased focus on mental health parity and access to care.",
                "intro": {
                    "content": "Psychiatric Nurses specialize in the intersection of physical and mental health. They manage psychotropic medications, conduct therapeutic communication, and ensure patient safety in acute or long-term psychiatric settings.",
                    "years": 4, "months": 0
                },
                "responsibilities": [
                    "Conducting mental health assessments and monitoring emotional and behavioral changes.",
                    "Administering and monitoring psychiatric medications, understanding complex Pharmacology & Medication Administration.",
                    "Leading therapeutic group sessions and providing individual counseling.",
                    "Managing crisis situations and intervening in high-risk scenarios (e.g., suicide watch).",
                    "Collaborating with psychiatrists, social workers, and psychologists.",
                    "Educating patients and families on coping mechanisms and illness management.",
                    "Using Clinical Assessment to monitor physical health status alongside mental health.",
                    "Ensuring adherence to legal and ethical guidelines regarding patient rights and involuntary commitment.",
                    "Documenting progress notes and treatment plans in EMR Management systems.",
                    "Advocating for reduced stigma and improved mental healthcare access."
                ],
                "specializations": [
                    ("Forensic Psychiatric Nurse", "Works with patients in correctional facilities or legal settings."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: General RN & Foundation",
                        "order": 1,
                        "description": "Complete BSN, pass NCLEX-RN. Gain experience in a general medical setting or a behavioral health unit.",
                        "education": ["Bachelor of Science in Nursing (BSN)"],
                        "skills": ["Clinical Assessment", "Pharmacology & Medication Administration", "Critical Thinking & Prioritization"],
                        "certifications": ["NCLEX-RN"],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: Specialty Practice",
                        "order": 2,
                        "description": "Work in an acute psychiatric unit. Master therapeutic communication and crisis intervention techniques.",
                        "education": [],
                        "skills": ["Patient Education & Advocacy"],
                        "certifications": [],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 3: Advanced Practice/MSN",
                        "order": 3,
                        "description": "Pursue MSN to become a Psychiatric Mental Health Nurse Practitioner (PMHNP), allowing for diagnosis and prescribing.",
                        "education": ["Master of Science in Nursing (MSN)"],
                        "skills": ["Advanced Pathophysiology", "Trauma & Emergency Response (ACLS/BLS)"],
                        "certifications": ["ANCC Board Certification (NP)"],
                        "specializations": ["Forensic Psychiatric Nurse"],
                    },
                    {
                        "name": "Phase 4: Therapy & Clinical Director",
                        "order": 4,
                        "description": "Establish an independent PMHNP practice or serve as Clinical Director for a mental health facility.",
                        "education": ["Doctor of Nursing Practice (DNP)"],
                        "skills": [],
                        "certifications": [],
                        "specializations": [],
                    }
                ]
            },

            # --- 6. NURSE ANESTHETIST (CRNA) ---
            "Nurse Anesthetist (CRNA)": {
                "overview": "Administers anesthesia and monitors patients throughout surgery, recovery, and pain management.",
                "salary": 2000000.00,
                "outlook": "High-salary, high-demand specialty; requires DNP (since 2025) and extensive critical care experience.",
                "intro": {
                    "content": "CRNAs are highly autonomous, highly skilled anesthesia providers. They require a minimum of one year of experience in an intensive care setting before applying to a competitive DNP program.",
                    "years": 8, "months": 0
                },
                "responsibilities": [
                    "Performing pre-anesthetic assessments and planning individualized anesthesia care.",
                    "Administering general, regional, and local anesthesia and sedation.",
                    "Monitoring patient vital signs, including complex cardiovascular and respiratory functions (Surgical/Anesthesia Monitoring).",
                    "Managing patient airways, intubation, and mechanical ventilation.",
                    "Collaborating with surgeons, dentists, and obstetricians.",
                    "Responding to critical events and managing acute pain (Trauma & Emergency Response).",
                    "Maintaining proficiency in Pharmacology & Medication Administration of anesthetic agents.",
                    "Documenting all physiological changes and anesthetic interventions.",
                    "Ensuring patient safety and comfort during the entire perioperative period.",
                    "Utilizing Advanced Pathophysiology to understand how co-morbidities affect anesthesia."
                ],
                "specializations": [
                    ("Cardiac CRNA", "Specializing in anesthesia for complex heart and vascular procedures."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: BSN & ICU Experience",
                        "order": 1,
                        "description": "Complete BSN, obtain RN license. Gain at least 1-2 years of full-time Critical Care Nurse (ICU) experience, mastering trauma and critical skills.",
                        "education": ["Bachelor of Science in Nursing (BSN)"],
                        "skills": ["Critical Thinking & Prioritization", "Trauma & Emergency Response (ACLS/BLS)", "Pharmacology & Medication Administration"],
                        "certifications": ["NCLEX-RN", "CCRN"],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: DNP Program Entry",
                        "order": 2,
                        "description": "Enroll in a DNP Nurse Anesthesia program (3-4 years). Focus on Advanced Pathophysiology, complex assessment, and Surgical/Anesthesia Monitoring.",
                        "education": ["Doctor of Nursing Practice (DNP)"],
                        "skills": ["Advanced Pathophysiology", "Surgical/Anesthesia Monitoring"],
                        "certifications": [],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 3: Certification & Practice",
                        "order": 3,
                        "description": "Pass the national certification exam and begin clinical practice as a CRNA. Master different types of anesthesia delivery.",
                        "education": [],
                        "skills": [],
                        "certifications": ["CRNA Certification"],
                        "specializations": ["Cardiac CRNA"],
                    },
                    {
                        "name": "Phase 4: Leadership & Education",
                        "order": 4,
                        "description": "Serve as Chief CRNA, Program Director for an anesthesia school, or specialize in a niche area like pain management.",
                        "education": [],
                        "skills": [],
                        "certifications": [],
                        "specializations": [],
                    }
                ]
            },

            # --- 7. ONCOLOGY NURSE ---
            "Oncology Nurse": {
                "overview": "Provides specialized care to cancer patients, managing treatment side effects and administering chemotherapy and radiation.",
                "salary": 820000.00,
                "outlook": "Consistent growth due to advances in cancer treatment and an aging population.",
                "intro": {
                    "content": "Oncology Nurses provide comprehensive care during one of the most challenging periods of a patient's life. They manage complex protocols, administer high-risk agents (Pharmacology & Medication Administration), and offer significant Patient Education & Advocacy.",
                    "years": 4, "months": 0
                },
                "responsibilities": [
                    "Administering chemotherapy and biotherapy agents safely, following strict protocols.",
                    "Monitoring and managing the toxic side effects of cancer treatments.",
                    "Providing extensive Patient Education & Advocacy on treatment plans, side effects, and self-care.",
                    "Managing central lines and specialized intravenous access.",
                    "Offering emotional and psychological support to patients and families.",
                    "Collaborating with oncologists, radiation therapists, and palliative care teams.",
                    "Utilizing Clinical Assessment skills to detect signs of infection or oncologic emergencies.",
                    "Participating in clinical trials and research related to cancer treatment.",
                    "Ensuring timely documentation of all treatments and patient responses.",
                    "Adhering to strict Infection Control & Sterilization procedures for immunocompromised patients."
                ],
                "specializations": [
                    ("Chemotherapy Certified Nurse", "Specializing in the safe preparation and administration of cytotoxic drugs."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: BSN & General Experience",
                        "order": 1,
                        "description": "Complete BSN, obtain RN license. Gain 1-2 years experience in Med-Surg or an infusion center to build core skills.",
                        "education": ["Bachelor of Science in Nursing (BSN)"],
                        "skills": ["Clinical Assessment", "Pharmacology & Medication Administration", "Patient Education & Advocacy"],
                        "certifications": ["NCLEX-RN"],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: Oncology Specialization",
                        "order": 2,
                        "description": "Work on an inpatient or outpatient oncology unit. Obtain ONS (Oncology Nursing Society) certification in chemotherapy/biotherapy administration.",
                        "education": [],
                        "skills": ["Infection Control & Sterilization", "Critical Thinking & Prioritization"],
                        "certifications": [],
                        "specializations": ["Chemotherapy Certified Nurse"],
                    },
                    {
                        "name": "Phase 3: Certification & Advanced Roles",
                        "order": 3,
                        "description": "Obtain OCN (Oncology Certified Nurse) certification. Move into roles like Navigator, coordinating complex care across multiple services.",
                        "education": [],
                        "skills": ["Trauma & Emergency Response (ACLS/BLS)"],
                        "certifications": [],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 4: Advanced Practice",
                        "order": 4,
                        "description": "Pursue an MSN to become an Oncology Nurse Practitioner, focusing on survivorship, acute symptom management, and clinical trials.",
                        "education": ["Master of Science in Nursing (MSN)"],
                        "skills": [],
                        "certifications": ["ANCC Board Certification (NP)"],
                        "specializations": [],
                    }
                ]
            },

            # --- 8. MIDWIFE (CNM) ---
            "Certified Nurse Midwife (CNM)": {
                "overview": "Provides gynecological exams, family planning, and comprehensive care for women throughout the reproductive cycle, including prenatal and birth care.",
                "salary": 1150000.00,
                "outlook": "Strong growth, driven by patient demand for natural birth options and preventative women's health.",
                "intro": {
                    "content": "CNMs are APRNs who focus on women's health in a holistic, preventative model. They manage low-risk pregnancies, deliver babies, and provide primary care to women from adolescence through menopause.",
                    "years": 6, "months": 0
                },
                "responsibilities": [
                    "Providing routine gynecological care and annual exams.",
                    "Managing low-risk prenatal, labor, delivery, and postpartum care.",
                    "Monitoring fetal heart rate and maternal progress during labor.",
                    "Ordering and interpreting laboratory and diagnostic tests.",
                    "Providing reproductive health counseling and family planning services.",
                    "Collaborating with OB/GYN physicians for high-risk pregnancies.",
                    "Utilizing Clinical Assessment skills specifically for maternal-fetal health.",
                    "Conducting newborn examinations and initial infant care.",
                    "Emphasizing Patient Education & Advocacy for informed consent and birth choices.",
                    "Performing minor procedures related to obstetrics."
                ],
                "specializations": [
                    ("Lactation Consultant", "Specializing in breastfeeding support and infant nutrition."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: RN & Women's Health Base",
                        "order": 1,
                        "description": "Complete BSN, obtain RN license. Gain 1-2 years experience in Labor & Delivery (L&D) or Postpartum units.",
                        "education": ["Bachelor of Science in Nursing (BSN)"],
                        "skills": ["Clinical Assessment", "Pharmacology & Medication Administration", "Trauma & Emergency Response (ACLS/BLS)"],
                        "certifications": ["NCLEX-RN"],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: Graduate Midwifery Study",
                        "order": 2,
                        "description": "Enroll in an MSN/DNP midwifery program. Master Advanced Pathophysiology related to pregnancy and childbirth.",
                        "education": ["Master of Science in Nursing (MSN)"],
                        "skills": ["Advanced Pathophysiology", "Patient Education & Advocacy", "Critical Thinking & Prioritization"],
                        "certifications": [],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 3: Certification & Independent Practice",
                        "order": 3,
                        "description": "Pass the AMCB certification exam and begin practicing as a CNM, managing a full scope of women's health services.",
                        "education": [],
                        "skills": [],
                        "certifications": ["ANCC Board Certification (NP)"],
                        "specializations": ["Lactation Consultant"],
                    },
                    {
                        "name": "Phase 4: Clinical Director",
                        "order": 4,
                        "description": "Serve as Director of Midwifery Services or lead community-based women's health initiatives.",
                        "education": ["Doctor of Nursing Practice (DNP)"],
                        "skills": [],
                        "certifications": [],
                        "specializations": [],
                    }
                ]
            },

            # --- 9. NURSING INFORMATICS SPECIALIST ---
            "Nursing Informatics Specialist": {
                "overview": "Integrates nursing science with information science to manage and communicate data, information, and knowledge in nursing practice.",
                "salary": 1050000.00,
                "outlook": "Very strong growth; essential for optimizing EMR systems and improving data-driven care.",
                "intro": {
                    "content": "Informatics Nurses bridge the gap between clinical care and technology. They optimize Electronic Medical Records (EMR) Management systems, ensure data security, and design efficient workflows for nurses and other clinicians.",
                    "years": 4, "months": 0
                },
                "responsibilities": [
                    "Leading the implementation and optimization of Electronic Medical Records (EMR) Management and other clinical systems.",
                    "Designing efficient clinical workflows and training staff on system use.",
                    "Analyzing clinical data to identify opportunities for quality improvement and patient safety.",
                    "Ensuring compliance with data privacy regulations (HIPAA) and utilizing Informatics & Data Security skills.",
                    "Serving as the liaison between the nursing staff and the IT department.",
                    "Developing clinical documentation standards and standardized terminology.",
                    "Participating in software testing and quality assurance prior to system deployment.",
                    "Utilizing Epidemiology & Biostatistics for large-scale data analysis and reporting.",
                    "Applying Critical Thinking & Prioritization to solve complex system and workflow issues.",
                    "Providing technical support and troubleshooting for clinical applications."
                ],
                "specializations": [
                    ("Clinical Workflow Analyst", "Specializing in process mapping and efficiency improvement within the hospital."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: Clinical RN & EMR Competency",
                        "order": 1,
                        "description": "Complete BSN, obtain RN license. Gain 2+ years of hands-on experience using EMR and Clinical Assessment skills at the bedside.",
                        "education": ["Bachelor of Science in Nursing (BSN)"],
                        "skills": ["Clinical Assessment", "Electronic Medical Records (EMR) Management", "Critical Thinking & Prioritization"],
                        "certifications": ["NCLEX-RN"],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: Formal Informatics Training",
                        "order": 2,
                        "description": "Obtain CPHIMS certification or pursue an MSN in Nursing Informatics. Master Informatics & Data Security principles and basic data analysis.",
                        "education": ["Master of Science in Nursing (MSN)"],
                        "skills": ["Informatics & Data Security", "Epidemiology & Biostatistics", "Patient Education & Advocacy"],
                        "certifications": ["CPHIMS"],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 3: System Leadership",
                        "order": 3,
                        "description": "Lead major EMR upgrades or module implementations. Focus on data governance and system integration.",
                        "education": [],
                        "skills": ["Advanced Pathophysiology", "Pharmacology & Medication Administration"],
                        "certifications": [],
                        "specializations": ["Clinical Workflow Analyst"],
                    },
                    {
                        "name": "Phase 4: CINO/Director Level",
                        "order": 4,
                        "description": "Transition to Chief Nursing Informatics Officer (CNIO) or Director of Clinical Systems, setting the organization’s strategic technology roadmap.",
                        "education": ["Doctor of Nursing Practice (DNP)"],
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
                        "sector": nursing_sector,
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

        self.stdout.write(self.style.SUCCESS('\nNursing data population complete! 9 careers successfully defined.'))
        