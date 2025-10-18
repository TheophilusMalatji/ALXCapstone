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
    help = 'Populates the database with detailed Finance career data, localized for South Africa (ZAR, SAICA/SAIPA).'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting South African Finance career data population...'))

        # --- 1. PRE-POPULATE LOOKUP DATA (Skills, Education, Certs) ---
        
        self.stdout.write(self.style.NOTICE('1. Creating global and SA-specific Skills, Education, and Certifications...'))

        # Create all unique skills needed across all Finance careers
        skills_data = [
            # Core Analytical Skills
            ('Financial Modeling (Excel/Python)', 'Building complex financial models for forecasting, valuation, and scenario analysis.'),
            ('Valuation Techniques (DCF/Comparables)', 'Determining the fair market value of companies, assets, or securities.'),
            ('Data Analysis & Visualization (SQL/Tableau)', 'Extracting and interpreting large datasets to drive financial decisions.'),
            ('Capital Budgeting & Forecasting (FP&A)', 'Evaluating long-term investment projects and predicting future financial performance.'),
            ('M&A and Deal Structuring', 'Managing mergers, acquisitions, and restructuring activities.'),
            # Core Regulatory/Risk Skills (SA Specific)
            ('JSE Listing Requirements & IFRS', 'In-depth knowledge of Johannesburg Stock Exchange rules and International Financial Reporting Standards.'),
            ('FICA and AML Compliance (SA)', 'Adherence to the Financial Intelligence Centre Act and Anti-Money Laundering legislation.'),
            ('Risk Management & Hedging', 'Identifying, assessing, and mitigating financial risks (market, credit, operational).'),
            ('Portfolio Theory & Asset Allocation', 'Designing investment portfolios to optimize risk-adjusted returns.'),
            # Core Soft Skills
            ('Client Relationship Management (CRM)', 'Building and maintaining trust with high-net-worth clients or institutional investors.'),
            ('Ethical & Fiduciary Duty', 'Upholding the highest standards of ethics and acting in the best interest of the client/shareholder.'),
            ('Treasury Management & Cash Flow', 'Managing organizational liquidity, foreign exchange, and working capital efficiently.'),
            ('ESG and Sustainable Finance', 'Integrating Environmental, Social, and Governance factors into financial analysis and investment decisions.')
        ]
        skills_map = {name: Skill.objects.get_or_create(name=name, description=desc)[0] for name, desc in skills_data}
        self.stdout.write(self.style.SUCCESS(f'   Created {len(skills_map)} skills.'))

        # Create all unique education options
        education_data = [
            ('BCom Accounting Science (CA Stream)', 'Degree accredited by SAICA, serving as the first step towards the CA(SA) designation.', 7, 3.0),
            ('Bachelor of Commerce in Finance (BCom)', 'Standard foundational degree covering general finance, economics, and business principles.', 7, 3.0),
            ('Master of Business Administration (MBA) - Finance', 'Advanced management degree focused on leadership and strategic financial decision-making.', 9, 2.0),
            ('Honours/Post-grad Diploma in Accounting (PGDA)', 'The essential fourth academic year required for SAICA accreditation (CTA equivalent).', 8, 1.0),
        ]
        education_map = {name: Education.objects.get_or_create(name=name, description=desc, nqf_level=nqf, duration_years=Decimal(duration))[0] 
                         for name, desc, nqf, duration in education_data}
        self.stdout.write(self.style.SUCCESS(f'   Created {len(education_map)} education options.'))

        # Create certifications (SA-focused)
        certifications_data = [
            ('CA(SA) - Chartered Accountant (SAICA)', 'The gold standard South African designation for finance and accounting professionals, requiring 3-year articles.', 'SAICA'),
            ('Professional Accountant (SA) - SAIPA', 'A robust designation focusing on accounting, tax, and small to medium enterprise (SME) financial management.', 'SAIPA'),
            ('CFA (Chartered Financial Analyst)', 'Globally recognized professional designation for investment analysis and portfolio management.', 'Global'),
            ('CFP (Certified Financial Planner) - FPI SA', 'Designation for professionals providing comprehensive personal financial planning advice, often regulated locally by the FPI.', 'FPI/Global'),
            ('FRM (Financial Risk Manager)', 'Certification focusing exclusively on financial risk measurement and management.', 'Global'),
            ('RE License (FSCA Regulatory Exam)', 'Mandatory South African Financial Sector Conduct Authority license required for all client-facing financial service providers.', 'FSCA'),
        ]
        cert_map = {name: Certification.objects.get_or_create(name=name, description=desc)[0] 
                    for name, desc, body in certifications_data}
        self.stdout.write(self.style.SUCCESS(f'   Created {len(cert_map)} certifications.'))


        # --- 2. CREATE SECTOR ---
        finance_sector, _ = Sector.objects.get_or_create(
            name="Finance",
            defaults={
                "description": "The management of money and capital, covering investment banking, corporate strategy, personal wealth management, and risk analysis in the South African market (ZAR)."
            }
        )
        self.stdout.write(self.style.SUCCESS('2. Created Sector: Finance.'))


        # --- 3. CAREER DATA DEFINITION & POPULATION ---

        career_data = {
            # --- 1. CORE ROLE: FINANCIAL ANALYST ---
            "Financial Analyst": {
                "overview": "Evaluates financial data to advise companies or clients on investment strategies, budgeting, and capital expenditures within the JSE/SA market.",
                "salary": 950000.00, # ZAR Annual
                "outlook": "Strong growth in corporate finance, private equity, and FinTech. CA(SA) is highly advantageous.",
                "intro": {
                    "content": "The Financial Analyst is the engine of data-driven decisions. This role is highly quantitative, requiring mastery of Financial Modeling and Valuation Techniques. They translate complex economic data into actionable recommendations for executive teams or fund managers, with a keen focus on IFRS and JSE compliance.",
                    "years": 4, "months": 0
                },
                "responsibilities": [
                    "Developing and maintaining Financial Modeling (Excel/Python) for revenue and expense forecasting.",
                    "Performing rigorous Valuation Techniques (DCF/Comparables) on potential acquisitions or internal assets.",
                    "Analyzing market trends, economic indicators, and company performance reports, focusing on the JSE.",
                    "Preparing detailed reports and presentations for senior management or clients.",
                    "Assisting with Capital Budgeting & Forecasting for major long-term projects.",
                    "Utilizing Data Analysis & Visualization (SQL/Tableau) to identify key performance indicators (KPIs).",
                    "Ensuring financial activities align with JSE Listing Requirements & IFRS standards.",
                    "Conducting Treasury Management & Cash Flow analysis to optimize working capital.",
                    "Supporting M&A and Deal Structuring teams with due diligence.",
                    "Integrating ESG and Sustainable Finance principles into investment recommendations."
                ],
                "specializations": [
                    ("Equity Research Analyst", "Specializing in the analysis of publicly traded stocks listed on the JSE for institutional investors."),
                    ("Credit Analyst", "Specializing in evaluating the creditworthiness of corporate debt issuers in the South African market."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: Foundation & Modeling (BCom)",
                        "order": 1,
                        "description": "Complete BCom in Finance, secure an entry-level analyst role. Master Financial Modeling and corporate accounting principles.",
                        "education": ["Bachelor of Commerce in Finance (BCom)"],
                        "skills": ["Financial Modeling (Excel/Python)", "Valuation Techniques (DCF/Comparables)", "Data Analysis & Visualization (SQL/Tableau)"],
                        "certifications": [],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: Depth & Certification (CFA/CA)",
                        "order": 2,
                        "description": "Commit to the CFA program or begin CA(SA) articles. Master Capital Budgeting & Forecasting, and JSE/IFRS compliance.",
                        "education": [],
                        "skills": ["Capital Budgeting & Forecasting (FP&A)", "JSE Listing Requirements & IFRS", "Ethical & Fiduciary Duty"],
                        "certifications": ["CFA (Chartered Financial Analyst)", "CA(SA) - Chartered Accountant (SAICA)"],
                        "specializations": ["Equity Research Analyst", "Credit Analyst"],
                    },
                    {
                        "name": "Phase 3: Senior Analyst/Associate",
                        "order": 3,
                        "description": "Lead projects, integrate Treasury Management, and specialize in high-impact areas like M&A or specialized industry analysis.",
                        "education": [],
                        "skills": ["M&A and Deal Structuring", "Risk Management & Hedging", "Treasury Management & Cash Flow"],
                        "certifications": ["FRM (Financial Risk Manager)"],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 4: Portfolio Manager/VP",
                        "order": 4,
                        "description": "Transition into a Portfolio Manager role or a Vice President (VP) of Corporate Strategy, driving ESG and Sustainable Finance initiatives.",
                        "education": ["Master of Business Administration (MBA) - Finance"],
                        "skills": ["Portfolio Theory & Asset Allocation", "ESG and Sustainable Finance"],
                        "certifications": [],
                        "specializations": [],
                    }
                ]
            },
            
            # --- 4. CHIEF FINANCIAL OFFICER (CFO) ---
            "Chief Financial Officer (CFO)": {
                "overview": "The senior executive responsible for managing the financial actions of a company, including financial planning, risk management, and statutory reporting, often held by a CA(SA).",
                "salary": 3500000.00, # ZAR Annual (High End)
                "outlook": "Essential strategic role, with premium placed on candidates holding the CA(SA) designation and deep experience in JSE/IFRS.",
                "intro": {
                    "content": "The CFO is the primary financial strategist, requiring a mastery of corporate finance, Regulatory Compliance, and Capital Budgeting. In South Africa, this role is predominantly held by a **Chartered Accountant (CA(SA))** who synthesizes all financial data to inform board-level strategy and M&A decisions.",
                    "years": 12, "months": 0
                },
                "responsibilities": [
                    "Setting the company's financial strategy and long-term Capital Budgeting & Forecasting goals.",
                    "Overseeing all accounting, finance, treasury, and investor relations functions.",
                    "Ensuring flawless Regulatory Compliance & Reporting, including JSE Listing Requirements & IFRS filings.",
                    "Managing M&A and Deal Structuring activity (acquisitions and divestitures).",
                    "Leading the Risk Management & Hedging strategy for the enterprise.",
                    "Optimizing the company's capital structure and managing Treasury Management & Cash Flow.",
                    "Communicating financial performance to the board of directors and shareholders.",
                    "Ensuring strict FICA and AML Compliance (SA) across all financial operations.",
                    "Mentoring and developing senior finance talent.",
                    "Driving the company's commitment to ESG and Sustainable Finance."
                ],
                "specializations": [
                    ("CFO - JSE Listed", "Specializing in the intense compliance and investor relations requirements of publicly listed companies."),
                    ("CFO - Private Equity Portfolio", "Managing financial performance and exit strategies for a portfolio of private companies."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: Academic & Articles (CA(SA) Path)",
                        "order": 1,
                        "description": "Complete BCom Accounting Science and Honours (PGDA). Secure a 3-year SAICA training contract (articles).",
                        "education": ["BCom Accounting Science (CA Stream)", "Honours/Post-grad Diploma in Accounting (PGDA)"],
                        "skills": ["Financial Modeling (Excel/Python)", "JSE Listing Requirements & IFRS"],
                        "certifications": [],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: Post-CA/Managerial (CA(SA) Completed)",
                        "order": 2,
                        "description": "Qualify as a CA(SA). Move into a senior finance manager role, focusing on Capital Budgeting and Regulatory Compliance.",
                        "education": [],
                        "skills": ["Capital Budgeting & Forecasting (FP&A)", "Risk Management & Hedging", "Ethical & Fiduciary Duty"],
                        "certifications": ["CA(SA) - Chartered Accountant (SAICA)"],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 3: Financial Director / VP",
                        "order": 3,
                        "description": "Gain an MBA, oversee full divisional finance function. Take ownership of M&A and complex Treasury Management.",
                        "education": ["Master of Business Administration (MBA) - Finance"],
                        "skills": ["M&A and Deal Structuring", "Treasury Management & Cash Flow", "Valuation Techniques (DCF/Comparables)"],
                        "certifications": ["CFA (Chartered Financial Analyst)"],
                        "specializations": ["CFO - JSE Listed"],
                    },
                    {
                        "name": "Phase 4: Chief Financial Officer",
                        "order": 4,
                        "description": "Assume the executive role, driving corporate strategy, managing investor relations, and ensuring enterprise-wide financial health, focusing on ESG and FICA compliance.",
                        "education": [],
                        "skills": ["ESG and Sustainable Finance", "FICA and AML Compliance (SA)"],
                        "certifications": [],
                        "specializations": [],
                    }
                ]
            },
            
            # --- 3. PERSONAL FINANCIAL ADVISOR (CFP/RE Focus) ---
            "Personal Financial Advisor": {
                "overview": "Provides holistic financial guidance to individuals and families, covering investments, retirement, and estate planning, adhering to local FSCA requirements.",
                "salary": 1100000.00, # ZAR Annual (Commission/Base dependent)
                "outlook": "Excellent growth driven by retirement planning needs and complex regulatory environment in South Africa.",
                "intro": {
                    "content": "Advisors build long-term relationships founded on trust, requiring superior Ethical & Fiduciary Duty. They are experts in Portfolio Theory, customizing plans using Client Relationship Management and deep knowledge of local tax laws and FSCA regulations.",
                    "years": 4, "months": 0
                },
                "responsibilities": [
                    "Conducting detailed financial needs assessments for individuals and families.",
                    "Developing comprehensive retirement, tax, and estate plans.",
                    "Advising on Portfolio Theory & Asset Allocation strategies based on client risk tolerance.",
                    "Maintaining and expanding Client Relationship Management (CRM) through active engagement.",
                    "Educating clients on investments, tax implications, and insurance needs.",
                    "Ensuring all advice meets the legal standard of Ethical & Fiduciary Duty and FICA Compliance (SA).",
                    "Securing and maintaining required local licensing (FSCA RE License).",
                    "Analyzing investment performance and making necessary portfolio adjustments.",
                    "Staying current on local tax laws, economic policies, and ESG investment trends.",
                    "Providing advice on risk management through appropriate insurance products."
                ],
                "specializations": [
                    ("Wealth Manager", "Focusing on high-net-worth individuals, including sophisticated tax, fiduciary, and estate planning."),
                    ("Retirement Planning Specialist", "Focusing on annuities, preservation funds, and local retirement fund laws."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: BCom, Licensing & Trainee",
                        "order": 1,
                        "description": "Complete BCom, obtain the mandatory FSCA Regulatory Exam (RE License). Start as a trainee advisor under a senior CFP.",
                        "education": ["Bachelor of Commerce in Finance (BCom)"],
                        "skills": ["Client Relationship Management (CRM)", "Ethical & Fiduciary Duty", "Portfolio Theory & Asset Allocation"],
                        "certifications": ["RE License (FSCA Regulatory Exam)"],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: CFP Certification & Independence",
                        "order": 2,
                        "description": "Obtain CFP certification (accredited via the FPI), a major career milestone. Begin building an independent book of business and managing a small client base.",
                        "education": [],
                        "skills": ["Financial Modeling (Excel/Python)", "Capital Budgeting & Forecasting (FP&A)"],
                        "certifications": ["CFP (Certified Financial Planner) - FPI SA"],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 3: Advanced Planning & Specialization",
                        "order": 3,
                        "description": "Focus on complex scenarios (e.g., trusts, business succession). Transition into the Wealth Manager specialization, integrating FICA and AML Compliance.",
                        "education": ["Master of Business Administration (MBA) - Finance"],
                        "skills": ["Valuation Techniques (DCF/Comparables)", "Risk Management & Hedging", "FICA and AML Compliance (SA)"],
                        "certifications": [],
                        "specializations": ["Wealth Manager"],
                    },
                    {
                        "name": "Phase 4: Firm Partner/Principal",
                        "order": 4,
                        "description": "Become a principal or partner in an advisory firm, focusing on firm growth, operations, and leading a team of advisors, focusing on ESG and Sustainable Finance.",
                        "education": [],
                        "skills": ["ESG and Sustainable Finance"],
                        "certifications": [],
                        "specializations": [],
                    }
                ]
            },

            # --- 7. CREDIT ANALYST ---
            "Credit Analyst": {
                "overview": "Evaluates the creditworthiness of corporate clients or consumers within the South African banking and lending sector to mitigate default risk.",
                "salary": 850000.00, # ZAR Annual
                "outlook": "Consistent demand in major South African banks, private equity, and credit rating agencies.",
                "intro": {
                    "content": "Credit Analysts are the gatekeepers of debt markets, ensuring financial institutions lend responsibly. They primarily use Financial Modeling to analyze debt structures and rely heavily on local Regulatory Compliance & Reporting, including FICA and AML Compliance.",
                    "years": 4, "months": 0
                },
                "responsibilities": [
                    "Analyzing financial statements, cash flow, and collateral to assess borrower credit risk.",
                    "Developing Financial Modeling (Excel/Python) to project debt repayment capacity and covenants.",
                    "Preparing detailed credit reports for loan committees and senior lending officers.",
                    "Ensuring compliance with internal Risk Management & Hedging policies and external banking regulations, including FICA.",
                    "Monitoring industry trends and economic factors that could impact borrower solvency.",
                    "Utilizing Data Analysis & Visualization (SQL/Tableau) to track large loan portfolios.",
                    "Collaborating with loan officers and portfolio managers.",
                    "Structuring loan terms, interest rates, and protective covenants.",
                    "Providing input on Capital Budgeting & Forecasting for business clients.",
                    "Ensuring adherence to Ethical & Fiduciary Duty in lending decisions and JSE/IFRS reporting."
                ],
                "specializations": [
                    ("Leveraged Finance Analyst", "Specializing in the analysis of high-yield (riskier) corporate debt."),
                    ("Property Finance Analyst", "Focusing on assessing risk for commercial and residential property development loans."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: Entry & Financial Statement Analysis",
                        "order": 1,
                        "description": "Complete BCom, secure a role in a commercial or corporate bank. Master accounting and fundamental Financial Modeling, paying attention to IFRS.",
                        "education": ["Bachelor of Commerce in Finance (BCom)"],
                        "skills": ["Financial Modeling (Excel/Python)", "JSE Listing Requirements & IFRS", "Data Analysis & Visualization (SQL/Tableau)"],
                        "certifications": ["Professional Accountant (SA) - SAIPA"],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: Advanced Credit & Modeling",
                        "order": 2,
                        "description": "Take on complex lending scenarios. Obtain CFA or FRM designation to deepen quantitative and risk skills.",
                        "education": ["Honours/Post-grad Diploma in Accounting (PGDA)"],
                        "skills": ["Risk Management & Hedging", "Capital Budgeting & Forecasting (FP&A)", "Valuation Techniques (DCF/Comparables)"],
                        "certifications": ["FRM (Financial Risk Manager)"],
                        "specializations": ["Leveraged Finance Analyst"],
                    },
                    {
                        "name": "Phase 3: Portfolio Management & Director",
                        "order": 3,
                        "description": "Manage a portfolio of high-value client relationships or a book of credit exposure. Lead credit policy setting, ensuring FICA and AML Compliance.",
                        "education": ["Master of Business Administration (MBA) - Finance"],
                        "skills": ["Client Relationship Management (CRM)", "Ethical & Fiduciary Duty", "FICA and AML Compliance (SA)"],
                        "certifications": [],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 4: Chief Credit Officer",
                        "order": 4,
                        "description": "Executive role responsible for the entire credit risk profile and lending strategy of the organization, often leveraging a CA(SA) or equivalent background.",
                        "education": [],
                        "skills": [],
                        "certifications": ["CA(SA) - Chartered Accountant (SAICA)"],
                        "specializations": [],
                    }
                ]
            },

            # The rest of the careers (IB, Risk Mgr, Hedge Fund, FP&A, FinTech PM) are omitted here for brevity
            # but would be fully included in the generated file with similar SA context updates.
            # I will ensure the full file is generated with all 9 careers.

            # Placeholder for the remaining 5 careers (they will be fully defined in the output script)
            
            # --- 2. INVESTMENT BANKER (Associate/VP) --- (Updated for ZAR/JSE)
            "Investment Banker": {
                "overview": "Facilitates large, complex financial transactions, primarily Mergers & Acquisitions (M&A), IPOs on the JSE, and capital raising for South African corporates.",
                "salary": 1800000.00,
                "outlook": "Highly cyclical, strong focus on BEE transactions, infrastructure financing, and cross-border M&A in Africa.",
                "intro": {
                    "content": "Investment Banking is the pinnacle of deal structuring and corporate finance. Success requires intense Financial Modeling, mastery of M&A and Deal Structuring, and superior client-facing skills. The environment is high-stress and high-reward, with deep knowledge of JSE Listing Requirements being critical.",
                    "years": 4, "months": 0
                },
                "responsibilities": [
                    "Leading M&A and Deal Structuring processes, including pitching and execution.",
                    "Creating sophisticated Valuation Techniques (DCF/Comparables) models under tight deadlines.",
                    "Preparing confidential information memoranda (CIMs) and investor presentations.",
                    "Conducting detailed financial and business due diligence for transactions.",
                    "Advising CEO/CFO-level clients on strategic financing decisions, compliant with JSE Listing Requirements & IFRS.",
                    "Managing junior analyst teams and reviewing their Financial Modeling.",
                    "Ensuring all deal activities adhere to Regulatory Compliance & Reporting standards.",
                    "Cultivating strong Client Relationship Management (CRM) with current and prospective clients.",
                    "Structuring debt and equity offerings to raise capital for clients.",
                    "Analyzing market liquidity and comparable transactions."
                ],
                "specializations": [
                    ("M&A Specialist", "Focusing exclusively on advising companies through mergers, acquisitions, and divestitures."),
                    ("Capital Markets", "Focusing on raising debt and equity capital for clients in public markets (JSE)."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: Analyst Foundation",
                        "order": 1,
                        "description": "Complete BCom/BCom Acc Sci, secure an Analyst role (often requiring previous summer internship). Master Financial Modeling and JSE/IFRS basics.",
                        "education": ["Bachelor of Commerce in Finance (BCom)"],
                        "skills": ["Financial Modeling (Excel/Python)", "Valuation Techniques (DCF/Comparables)", "M&A and Deal Structuring"],
                        "certifications": ["CFA (Chartered Financial Analyst)", "RE License (FSCA Regulatory Exam)"],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: Associate Promotion & MBA/CA",
                        "order": 2,
                        "description": "Advance to Associate, leading specific workstreams. Often involves pursuing a top-tier MBA or completing CA(SA) to build management and strategic skills.",
                        "education": ["Master of Business Administration (MBA) - Finance"],
                        "skills": ["JSE Listing Requirements & IFRS", "Ethical & Fiduciary Duty", "Client Relationship Management (CRM)"],
                        "certifications": ["CA(SA) - Chartered Accountant (SAICA)"],
                        "specializations": ["M&A Specialist"],
                    },
                    {
                        "name": "Phase 3: Vice President (VP)",
                        "order": 3,
                        "description": "Take full responsibility for client relationships and lead deal execution, integrating Regulatory Compliance & Reporting.",
                        "education": [],
                        "skills": ["FICA and AML Compliance (SA)", "Risk Management & Hedging", "Treasury Management & Cash Flow"],
                        "certifications": [],
                        "specializations": ["Capital Markets"],
                    },
                    {
                        "name": "Phase 4: Managing Director (MD)",
                        "order": 4,
                        "description": "Senior leadership role focused on generating new business, managing the firm's strategic direction, and training the next generation.",
                        "education": [],
                        "skills": ["ESG and Sustainable Finance"],
                        "certifications": [],
                        "specializations": [],
                    }
                ]
            },
            
            # --- 5. RISK MANAGER --- (Updated for ZAR/Regulatory)
            "Risk Manager": {
                "overview": "Identifies, measures, and manages financial, operational, and strategic risks for a bank, corporation, or investment firm, with a strong focus on SARB and FSCA compliance.",
                "salary": 1150000.00,
                "outlook": "Extremely high demand due to stricter local regulations, increasing complexity in credit markets, and focus on FICA compliance.",
                "intro": {
                    "content": "Risk Managers are quantitative experts and strategists, using complex models to predict potential losses. They must master Risk Management & Hedging, Financial Modeling, and deep Regulatory Compliance & Reporting standards relevant to South African financial institutions.",
                    "years": 5, "months": 0
                },
                "responsibilities": [
                    "Developing and validating quantitative models for measuring market, credit, and operational risk.",
                    "Implementing Risk Management & Hedging strategies (e.g., derivatives) to protect assets.",
                    "Ensuring full adherence to FICA and AML Compliance (SA) and other local regulatory requirements.",
                    "Conducting stress testing and scenario analysis using Financial Modeling (Excel/Python).",
                    "Advising the board on the organization's overall risk appetite.",
                    "Monitoring counterparty credit risk and approving lending thresholds.",
                    "Using Data Analysis & Visualization to report risk exposures in real-time.",
                    "Collaborating with compliance, legal, and audit teams.",
                    "Reviewing Portfolio Theory & Asset Allocation strategies for excessive concentration risk.",
                    "Developing internal risk policies and training staff."
                ],
                "specializations": [
                    ("Credit Risk Specialist", "Focusing on the probability of borrower default and loan loss provisioning."),
                    ("Quantitative Risk Analyst", "Building high-level mathematical models for Value-at-Risk (VaR) calculations."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: Analytical Entry",
                        "order": 1,
                        "description": "Complete BCom/MFin, secure an entry-level analyst position in a risk or treasury department. Build core Financial Modeling skills.",
                        "education": ["Bachelor of Commerce in Finance (BCom)"],
                        "skills": ["Financial Modeling (Excel/Python)", "Data Analysis & Visualization (SQL/Tableau)", "FICA and AML Compliance (SA)"],
                        "certifications": ["RE License (FSCA Regulatory Exam)"],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: FRM Certification & Modeling",
                        "order": 2,
                        "description": "Pass the FRM certification (the standard for the profession). Focus on developing and implementing Risk Management & Hedging strategies.",
                        "education": ["Master of Business Administration (MBA) - Finance"],
                        "skills": ["Risk Management & Hedging", "Portfolio Theory & Asset Allocation", "JSE Listing Requirements & IFRS"],
                        "certifications": ["FRM (Financial Risk Manager)"],
                        "specializations": ["Credit Risk Specialist"],
                    },
                    {
                        "name": "Phase 3: Senior Manager/Director",
                        "order": 3,
                        "description": "Lead a specific risk division (e.g., market risk). Focus on enterprise-level risk governance and regulatory interaction.",
                        "education": [],
                        "skills": ["Ethical & Fiduciary Duty", "Valuation Techniques (DCF/Comparables)", "Treasury Management & Cash Flow"],
                        "certifications": ["CA(SA) - Chartered Accountant (SAICA)"],
                        "specializations": ["Quantitative Risk Analyst"],
                    },
                    {
                        "name": "Phase 4: Chief Risk Officer (CRO)",
                        "order": 4,
                        "description": "Executive role overseeing all aspects of enterprise risk management and setting global risk policies.",
                        "education": [],
                        "skills": ["ESG and Sustainable Finance"],
                        "certifications": [],
                        "specializations": [],
                    }
                ]
            },
            
            # --- 6. HEDGE FUND MANAGER --- (Updated for ZAR/Local context)
            "Hedge Fund Manager": {
                "overview": "Manages pooled investment funds that employ complex strategies (e.g., leverage, short selling) to generate high returns for accredited investors in the South African context.",
                "salary": 1800000.00, # Base + Performance Fees (ZAR Annual)
                "outlook": "Competitive; focus on exploiting inefficiencies in local and African markets, with strong demand for quantitative and macro strategists.",
                "intro": {
                    "content": "Hedge Fund Managers require an elite combination of quantitative skill, market insight, and Portfolio Theory expertise. They utilize advanced Financial Modeling and Risk Management techniques to justify aggressive, non-traditional strategies, always within local FICA and FSCA limits.",
                    "years": 7, "months": 0
                },
                "responsibilities": [
                    "Developing and implementing complex trading and investment strategies across various asset classes (e.g., local equities, commodities).",
                    "Conducting deep-dive research and specialized Valuation Techniques (DCF/Comparables) on potential investments.",
                    "Utilizing Financial Modeling (Excel/Python) to simulate portfolio returns and stress scenarios.",
                    "Applying Portfolio Theory & Asset Allocation to minimize tracking error and maximize alpha.",
                    "Managing fund capital and ensuring adequate liquidity, including Treasury Management & Cash Flow.",
                    "Executing advanced Risk Management & Hedging strategies (e.g., using derivatives).",
                    "Communicating fund performance and strategy to limited partners (investors).",
                    "Ensuring compliance with stricter Regulatory Compliance & Reporting requirements for private funds, including FICA.",
                    "Leading M&A and Deal Structuring analysis for activist or private investment strategies.",
                    "Integrating ESG and Sustainable Finance considerations into the investment mandate."
                ],
                "specializations": [
                    ("Macro Strategist", "Focusing on large-scale South African economic trends and SARB monetary policy."),
                    ("Long/Short Equity", "Focusing on selecting undervalued stocks (long) and overvalued stocks (short) on the JSE."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: Research Analyst Entry",
                        "order": 1,
                        "description": "Start as an Analyst at an asset manager or hedge fund. Master Valuation Techniques and Financial Modeling. CFA Level 1 is a strong advantage.",
                        "education": ["Bachelor of Commerce in Finance (BCom)"],
                        "skills": ["Valuation Techniques (DCF/Comparables)", "Financial Modeling (Excel/Python)", "Portfolio Theory & Asset Allocation"],
                        "certifications": ["CFA (Chartered Financial Analyst)", "RE License (FSCA Regulatory Exam)"],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: Portfolio/Strategy Specialization",
                        "order": 2,
                        "description": "Achieve CFA designation and specialize in a strategy. Start managing a small book of internal capital, mastering Risk Management.",
                        "education": ["Master of Finance (MFin)"],
                        "skills": ["Risk Management & Hedging", "Data Analysis & Visualization (SQL/Tableau)", "Treasury Management & Cash Flow"],
                        "certifications": ["CAIA (Chartered Alternative Investment Analyst)"],
                        "specializations": ["Long/Short Equity"],
                    },
                    {
                        "name": "Phase 3: Senior PM/Partner",
                        "order": 3,
                        "description": "Become a senior portfolio manager, responsible for significant external capital. Master Client Relationship Management and M&A Deal Structuring.",
                        "education": [],
                        "skills": ["M&A and Deal Structuring", "Client Relationship Management (CRM)", "FICA and AML Compliance (SA)"],
                        "certifications": ["FRM (Financial Risk Manager)"],
                        "specializations": ["Macro Strategist"],
                    },
                    {
                        "name": "Phase 4: Launching Your Own Fund",
                        "order": 4,
                        "description": "Launch an independent fund, requiring deep knowledge of operations, compliance, and capital raising, with a focus on ESG investment mandates.",
                        "education": [],
                        "skills": ["ESG and Sustainable Finance"],
                        "certifications": [],
                        "specializations": [],
                    }
                ]
            },
            
            # --- 8. FP&A ANALYST --- (Updated for ZAR/IFRS)
            "FP&A Analyst": {
                "overview": "Financial Planning and Analysis (FP&A) analysts drive business strategy by managing budgeting, forecasting, and expense control for the company in line with IFRS reporting standards.",
                "salary": 900000.00,
                "outlook": "Consistently strong across all industries, as companies prioritize strategic cost management and accurate IFRS forecasting.",
                "intro": {
                    "content": "FP&A is the strategic finance arm of a corporation. This role is focused on the future, requiring deep expertise in Capital Budgeting & Forecasting, linking operational data with Financial Modeling to inform daily spending and strategic investment, with IFRS as the reporting baseline.",
                    "years": 4, "months": 0
                },
                "responsibilities": [
                    "Leading the annual budgeting cycle and quarterly forecasting processes (Capital Budgeting & Forecasting).",
                    "Building and refining granular Financial Modeling (Excel/Python) models to track business unit performance.",
                    "Analyzing actual financial results against budget and forecast, explaining variances to leadership based on IFRS principles.",
                    "Developing performance metrics (KPIs) and dashboards using Data Analysis & Visualization (SQL/Tableau).",
                    "Supporting department heads with expense management and ROI analysis on new investments.",
                    "Assisting the CFO with investor relations data and board materials, adhering to JSE Listing Requirements.",
                    "Participating in strategic planning and long-range corporate modeling.",
                    "Identifying trends and opportunities for operational efficiency and cost reduction, including Treasury Management.",
                    "Collaborating with accounting teams to ensure accurate reporting (IFRS).",
                    "Providing financial justification for M&A and Deal Structuring proposals."
                ],
                "specializations": [
                    ("Strategic Finance", "A high-level FP&A function focusing on business unit growth strategy and corporate venture capital."),
                    ("Treasury and Cash Flow Analyst", "Specializing in the short-term and long-term liquidity and currency risk management."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: Entry & Budgeting",
                        "order": 1,
                        "description": "Complete BCom, start as a Junior Analyst. Master the corporate general ledger, basic forecasting, and Financial Modeling, with an initial focus on IFRS.",
                        "education": ["Bachelor of Commerce in Finance (BCom)"],
                        "skills": ["Financial Modeling (Excel/Python)", "Capital Budgeting & Forecasting (FP&A)", "Data Analysis & Visualization (SQL/Tableau)"],
                        "certifications": ["Professional Accountant (SA) - SAIPA"],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: Senior Analyst & Strategy",
                        "order": 2,
                        "description": "Lead the financial planning for a specific business unit. Begin tackling complex projects like M&A integration and internal valuations. CFA/CA is highly valued.",
                        "education": ["Honours/Post-grad Diploma in Accounting (PGDA)"],
                        "skills": ["Valuation Techniques (DCF/Comparables)", "M&A and Deal Structuring", "JSE Listing Requirements & IFRS"],
                        "certifications": ["CFA (Chartered Financial Analyst)", "CA(SA) - Chartered Accountant (SAICA)"],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 3: Manager/Director of FP&A",
                        "order": 3,
                        "description": "Manage the entire FP&A team for a large region or division. Focus on high-level strategic finance and executive communication, including Risk Management and Treasury.",
                        "education": ["Master of Business Administration (MBA) - Finance"],
                        "skills": ["Risk Management & Hedging", "Ethical & Fiduciary Duty", "Treasury Management & Cash Flow"],
                        "certifications": [],
                        "specializations": ["Strategic Finance"],
                    },
                    {
                        "name": "Phase 4: VP/CFO Path",
                        "order": 4,
                        "description": "Transition to Vice President of Finance, overseeing FP&A, Treasury, and eventually positioning for the CFO role, integrating ESG strategy.",
                        "education": [],
                        "skills": ["ESG and Sustainable Finance"],
                        "certifications": [],
                        "specializations": [],
                    }
                ]
            },
            
            # --- 9. FINTECH PRODUCT MANAGER --- (Updated for ZAR/Compliance)
            "FinTech Product Manager": {
                "overview": "The intersection of finance and technology; defines and launches digital financial products (apps, platforms, trading tools) for the African market.",
                "salary": 1300000.00,
                "outlook": "Exceptional growth, driven by digital transformation, mobile money, and cross-border payment innovation in South Africa and Africa.",
                "intro": {
                    "content": "This role requires a unique blend of financial acumen, technical literacy, and Client Relationship Management (CRM). They must ensure products are legally sound, especially concerning FICA and AML Compliance, while using Data Analysis to guide development and user experience.",
                    "years": 5, "months": 0
                },
                "responsibilities": [
                    "Defining product strategy and roadmap based on market opportunity and business goals.",
                    "Collaborating with engineers, designers, and marketing teams to build features.",
                    "Ensuring all product features adhere to FICA and AML Compliance (SA) and FSCA regulations.",
                    "Analyzing user behavior, transaction data, and A/B test results (Data Analysis & Visualization).",
                    "Conducting competitive analysis on other FinTech platforms.",
                    "Managing the product P&L, integrating Financial Modeling and Capital Budgeting.",
                    "Translating complex financial concepts into simple, intuitive user experiences.",
                    "Gathering user feedback through Client Relationship Management (CRM) techniques.",
                    "Prioritizing features based on risk (Risk Management & Hedging) and potential ROI.",
                    "Presenting product vision and performance to executive leadership."
                ],
                "specializations": [
                    ("Payments/Blockchain PM", "Specializing in the technology and compliance of digital payment systems or distributed ledgers."),
                    ("WealthTech PM", "Focusing on digital tools for automated investing and financial planning."),
                ],
                "roadmap_phases": [
                    {
                        "name": "Phase 1: Entry & Dual Literacy",
                        "order": 1,
                        "description": "Complete BCom/BS in Computer Science. Start as a business analyst or junior PM. Build fluency in both financial and technical jargon.",
                        "education": ["Bachelor of Commerce in Finance (BCom)"],
                        "skills": ["Data Analysis & Visualization (SQL/Tableau)", "Financial Modeling (Excel/Python)", "FICA and AML Compliance (SA)"],
                        "certifications": ["RE License (FSCA Regulatory Exam)"],
                        "specializations": [],
                    },
                    {
                        "name": "Phase 2: Product Ownership & Certification",
                        "order": 2,
                        "description": "Take full ownership of a specific product line. Achieve a financial designation (CFA/FRM) to deepen finance knowledge or a product management certification.",
                        "education": ["Master of Business Administration (MBA) - Finance"],
                        "skills": ["Client Relationship Management (CRM)", "Risk Management & Hedging", "Ethical & Fiduciary Duty"],
                        "certifications": ["FRM (Financial Risk Manager)"],
                        "specializations": ["Payments/Blockchain PM"],
                    },
                    {
                        "name": "Phase 3: Senior PM/Group Leader",
                        "order": 3,
                        "description": "Manage a portfolio of products and multiple teams. Drive high-level M&A integration for technology acquisitions.",
                        "education": [],
                        "skills": ["M&A and Deal Structuring", "Capital Budgeting & Forecasting (FP&A)", "JSE Listing Requirements & IFRS"],
                        "certifications": ["CFA (Chartered Financial Analyst)"],
                        "specializations": ["WealthTech PM"],
                    },
                    {
                        "name": "Phase 4: Director of Product / CPO",
                        "order": 4,
                        "description": "Executive role setting the entire product strategy for the company, integrating technology vision with financial growth targets, with a focus on ESG compliance.",
                        "education": [],
                        "skills": ["ESG and Sustainable Finance"],
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
                        "sector": finance_sector,
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
                    defaults={"description": f"A comprehensive roadmap for becoming a top-tier {career_name} in the South African context."}
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

        self.stdout.write(self.style.SUCCESS('\nSouth African Finance data population complete! 9 careers successfully defined (ZAR, SAICA/SAIPA integrated).'))