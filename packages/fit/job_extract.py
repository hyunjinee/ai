import os
import textwrap
import langextract as lx

# API 키 설정
LANGEXTRACT_API_KEY = os.getenv("GOOGLE_AI_STUDIO")
os.environ["LANGEXTRACT_API_KEY"] = LANGEXTRACT_API_KEY

공고 = """
Acceleration Team Leader
토스 소속
정규직
합류하게 될 팀에 대해 알려드려요

Acceleration Team의 미션은 토스팀의 성장을 가속화하는 것이에요.
미션을 달성하기 위해 토스팀의 우선순위 높은 신규 사업을 scale하거나, 기존 사업에 새로운 비즈니스 모델을 추가하거나, 조직간 시너지 효과를 극대화하는 업무를 수행하고 있어요.
팀원들은 Private Equity, 전략컨설팅, 사업개발, FP&A 등 다양한 백그라운드를 가진 분들로 구성되어 있어요.
합류하면 함께할 업무예요

토스에서 이루어지는 다양한 신규 사업, 기존 사업의 성장을 가속화하는 프로젝트들을 설계하고, 이를 리드해요.
임팩트를 만들어낼 수 있는 크고 작은 전략을 수립하고, 목표와 액션 아이템을 정의해요.
액션 아이템 실행을 위해 비즈니스모델 설계, 파트너십, 세일즈, 제품 개발 등을 직접 수행하거나 관련 팀의 협업을 이끌어내요.
프로젝트의 에자일한 실행을 통해 전략과 실행 방향성을 수정하면서, 성공을 위한 방정식을 찾아내요.
본질적으로 업무 영역이 광범위하기 때문에 토스팀 리더, 각 사업부의 제품, 비즈니스, 전략, 더 나아가 계열사의 다양한 구성원들과 협력하게 되어요.
팀 리더로서 팀의 업무를 발굴하고 팀원들을 지원하며, 팀의 역할 확장에 기여해요.
이런 분과 함께하고 싶어요

Private Equity 피투자회사, 빅테크, 스타트업의 기획/전략/Corp Dev/Staff 조직 경험을 보유하신 분을 선호해요.
다양한 프로젝트의 리딩과 실행을 통해 임팩트를 만들어본 경험이 필수적으로 요구되어요.
플랫폼 비즈니스 모델에 대한 경험과 이해를 가지신 분이면 좋아요. 물론 오셔서 같이 배워 나가실 분도 환영해요.
팀을 이끌어본 리더십 경험이 있으시면 더욱 좋아요.
다음 역량을 갖추신 분을 찾고 있어요

Goal&action item setting: 크고 작은 사업의 목표를 설정하고, 이를 달성하기 위한 액션 아이템을 도출하는 역량
Execution: 액션 아이템을 다양한 방식으로 실행하여 임팩트를 만들어내는 역량
Project leading: 대내외의 이해관계자들을 조율하여 프로젝트를 리딩하는 역량
Flexibility: 프로젝트 수행 과정에서 발생하는 변수와 변화에 빠르게 대응하는 역량
Leadership: 인재들을 규합하여 동기부여하고, 팀과 팀원들의 역할 확장을 이끌어내는 역량
토스로의 합류 여정

서류 접수 > 커피챗 > 직무 인터뷰 > 문화적합성 인터뷰 > 레퍼런스 체크 > 처우 협의 > 최종 합격 및 입사
"""

# 채용공고에서 추출할 정보를 위한 프롬프트 정의
prompt = textwrap.dedent("""\
채용공고에서 회사명, 직무명, 팀명, 고용형태, 업무내용, 자격요건, 필요역량, 채용과정을 추출하세요.
정확한 텍스트를 사용하여 추출하고, 의역하거나 중복되는 항목은 피하세요.
각 추출 항목에 대해 의미있는 속성을 제공하여 맥락을 추가하세요.""")

# 고품질 예시 제공
examples = [
    lx.data.ExampleData(
        text=(
            "카카오 소속 Data Scientist 정규직 포지션입니다. "
            "머신러닝 모델 개발 경험이 필요하며, Python 사용 능력이 필수입니다. "
            "서류전형 > 1차면접 > 2차면접 > 최종합격 순으로 진행됩니다."
        ),
        extractions=[
            lx.data.Extraction(
                extraction_class="company",
                extraction_text="카카오",
                attributes={"type": "IT회사"},
            ),
            lx.data.Extraction(
                extraction_class="position",
                extraction_text="Data Scientist",
                attributes={"field": "데이터분석"},
            ),
            lx.data.Extraction(
                extraction_class="employment_type",
                extraction_text="정규직",
                attributes={"status": "풀타임"},
            ),
            lx.data.Extraction(
                extraction_class="requirement",
                extraction_text="머신러닝 모델 개발 경험",
                attributes={"category": "필수경험"},
            ),
            lx.data.Extraction(
                extraction_class="skill",
                extraction_text="Python",
                attributes={"level": "필수"},
            ),
            lx.data.Extraction(
                extraction_class="process",
                extraction_text="서류전형 > 1차면접 > 2차면접 > 최종합격",
                attributes={"steps": "4단계"},
            ),
        ],
    )
]

# 정보 추출 실행
result = lx.extract(
    text_or_documents=공고,
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-flash",
)

print("=" * 50)
print("토스 Acceleration Team Leader 채용공고 정보 추출 결과")
print("=" * 50)

# 추출된 정보를 카테고리별로 정리
categories = {
    "company": "회사 정보",
    "position": "직무 정보", 
    "team": "팀 정보",
    "employment_type": "고용 형태",
    "job_description": "업무 내용",
    "requirement": "자격 요건",
    "skill": "필요 역량",
    "process": "채용 과정"
}

for category, category_name in categories.items():
    category_items = [ex for ex in result.extractions if ex.extraction_class == category]
    if category_items:
        print(f"\n📌 {category_name}:")
        for item in category_items:
            print(f"  • {item.extraction_text}")
            if item.attributes:
                for key, value in item.attributes.items():
                    print(f"    - {key}: {value}")

print("\n" + "=" * 50)
print("전체 추출된 항목 수:", len(result.extractions))
print("=" * 50)