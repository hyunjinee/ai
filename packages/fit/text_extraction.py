import os
import textwrap
import langextract as lx

LANGEXTRACT_API_KEY = os.getenv("GOOGLE_AI_STUDIO")
os.environ["LANGEXTRACT_API_KEY"] = LANGEXTRACT_API_KEY

print(LANGEXTRACT_API_KEY)

# 1. Define a concise prompt
prompt = textwrap.dedent("""\
Extract characters, emotions, and relationships in order of appearance.
Use exact text for extractions. Do not paraphrase or overlap entities.
Provide meaningful attributes for each entity to add context.""")

# 2. Provide a high-quality example to guide the model
examples = [
    lx.data.ExampleData(
        text=(
            "ROMEO. But soft! What light through yonder window breaks? It is"
            " the east, and Juliet is the sun."
        ),
        extractions=[
            lx.data.Extraction(
                extraction_class="character",
                extraction_text="ROMEO",
                attributes={"emotional_state": "wonder"},
            ),
            lx.data.Extraction(
                extraction_class="emotion",
                extraction_text="But soft!",
                attributes={"feeling": "gentle awe"},
            ),
            lx.data.Extraction(
                extraction_class="relationship",
                extraction_text="Juliet is the sun",
                attributes={"type": "metaphor"},
            ),
        ],
    )
]

# 3. Run the extraction on your input text
input_text = (
    "Lady Juliet gazed longingly at the stars, her heart aching for Romeo"
)
result = lx.extract(
    text_or_documents=input_text,
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-pro",
)
print(result )


TC_ARTICLE = """Shortly after Hunter Lightman joined OpenAI as a researcher in 2022, he watched his colleagues launch ChatGPT, one of the fastest-growing products ever. Meanwhile, Lightman quietly worked on a team teaching OpenAI’s models to solve high school math competitions.

Today that team, known as MathGen, is considered instrumental to OpenAI’s industry-leading effort to create AI reasoning models: the core technology behind AI agents that can do tasks on a computer like a human would.

“We were trying to make the models better at mathematical reasoning, which at the time they weren’t very good at,” Lightman told TechCrunch, describing MathGen’s early work.

OpenAI’s models are far from perfect today — the company’s latest AI systems still hallucinate and its agents struggle with complex tasks.

But its state-of-the-art models have improved significantly on mathematical reasoning. One of OpenAI’s models recently won a gold medal at the International Math Olympiad, a math competition for the world’s brightest high school students. OpenAI believes these reasoning capabilities will translate to other subjects, and ultimately power general-purpose agents that the company has always dreamed of building.

ChatGPT was a happy accident — a lowkey research preview turned viral consumer business — but OpenAI’s agents are the product of a years-long, deliberate effort within the company.

“Eventually, you’ll just ask the computer for what you need and it’ll do all of these tasks for you,” said OpenAI CEO Sam Altman at the company’s first developer conference in 2023. “These capabilities are often talked about in the AI field as agents. The upsides of this are going to be tremendous.”

Whether agents will meet Altman’s vision remains to be seen, but OpenAI shocked the world with the release of its first AI reasoning model, o1, in the fall of 2024. Less than a year later, the 21 foundational researchers behind that breakthrough are the most highly sought-after talent in Silicon Valley.

Mark Zuckerberg recruited five of the o1 researchers to work on Meta’s new superintelligence-focused unit, offering some compensation packages north of $100 million. One of them, Shengjia Zhao, was recently named chief scientist of Meta Superintelligence Labs.

The reinforcement learning renaissance
The rise of OpenAI’s reasoning models and agents are tied to a machine learning training technique known as reinforcement learning (RL). RL provides feedback to an AI model on whether its choices were correct or not in simulated environments.

RL has been used for decades. For instance, in 2016, about a year after OpenAI was founded in 2015, an AI system created by Google DeepMind using RL, AlphaGo, gained global attention after beating a world champion in the board game, Go.

By 2018, OpenAI pioneered its first large language model in the GPT series, pretrained on massive amounts of internet data and a large clusters of GPUs. GPT models excelled at text processing, eventually leading to ChatGPT, but struggled with basic math.

It took until 2023 for OpenAI to achieve a breakthrough, initially dubbed “Q*” and then “Strawberry,” by combining LLMs, RL, and a technique called test-time computation. The latter gave the models extra time and computing power to plan and work through problems, verifying its steps, before providing an answer.

This allowed OpenAI to introduce a new approach called “chain-of-thought” (CoT), which improved AI’s performance on math questions the models hadn’t seen before.

“I could see the model starting to reason,” said El Kishky. “It would notice mistakes and backtrack, it would get frustrated. It really felt like reading the thoughts of a person.”

Though individually these techniques weren’t novel, OpenAI uniquely combined them to create Strawberry, which directly led to the development of o1. OpenAI quickly identified that the planning and fact checking abilities of AI reasoning models could be useful to power AI agents.

“We had solved a problem that I had been banging my head against for a couple of years,” said Lightman. “It was one of the most exciting moments of my research career.”

Scaling reasoning
With AI reasoning models, OpenAI determined it had two new axes that would allow it to improve AI models: using more computational power during the post-training of AI models, and giving AI models more time and processing power while answering a question.

“OpenAI, as a company, thinks a lot about not just the way things are, but the way things are going to scale,” said Lightman.

Shortly after the 2023 Strawberry breakthrough, OpenAI spun up an “Agents” team led by OpenAI researcher Daniel Selsam to make further progress on this new paradigm, two sources told TechCrunch. Although the team was called “Agents,”  OpenAI didn’t initially differentiate between reasoning models and agents as we think of them today. The company just wanted to make AI systems capable of completing complex tasks.

Eventually, the work of Selsam’s Agents team became part of a larger project to develop the o1 reasoning model, with leaders including OpenAI co-founder Ilya Sutskever, chief research officer Mark Chen, and chief scientist Jakub Pachocki.

OpenAI would have to divert precious resources — mainly talent and GPUs — to create o1. Throughout OpenAI’s history, researchers have had to negotiate with company leaders to obtain resources; demonstrating breakthroughs was a surefire way to secure them.

“One of the core components of OpenAI is that everything in research is bottom up,” said Lightman. “When we showed the evidence [for o1], the company was like, ‘This makes sense, let’s push on it.’”

Some former employees say that the startup’s mission to develop AGI was the key factor in achieving breakthroughs around AI reasoning models. By focusing on developing the smartest-possible AI models, rather than products, OpenAI was able to prioritize o1 above other efforts. That type of large investment in ideas wasn’t always possible at competing AI labs.

The decision to try new training methods proved prescient. By late 2024, several leading AI labs started seeing diminishing returns on models created through traditional pretraining scaling. Today, much of the AI field’s momentum comes from advances in reasoning models.

What does it mean for an AI to “reason?”
In many ways, the goal of AI research is to recreate human intelligence with computers. Since the launch of o1, ChatGPT’s UX has been filled with more human-sounding features such as “thinking” and “reasoning.”

When asked whether OpenAI’s models were truly reasoning, El Kishky hedged, saying he thinks about the concept in terms of computer science.

“We’re teaching the model how to efficiently expend compute to get an answer. So if you define it that way, yes, it is reasoning,” said El Kishky.

Lightman takes the approach of focusing on the model’s results and not as much on the means or their relation to human brains.

“If the model is doing hard things, then it is doing whatever necessary approximation of reasoning it needs in order to do that,” said Lightman. “We can call it reasoning, because it looks like these reasoning traces, but it’s all just a proxy for trying to make AI tools that are really powerful and useful to a lot of people.”

OpenAI’s researchers note people may disagree with their nomenclature or definitions of reasoning — and surely, critics have emerged — but they argue it’s less important than the capabilities of their models. Other AI researchers tend to agree.

Nathan Lambert, an AI researcher with the non-profit AI2, compares AI reasoning modes to airplanes in a blog post. Both, he says, are manmade systems inspired by nature — human reasoning and bird flight, respectively — but they operate through entirely different mechanisms. That doesn’t make them any less useful, or any less capable of achieving similar outcomes.

A group of AI researchers from OpenAI, Anthropic, and Google DeepMind agreed in a recent position paper that AI reasoning models are not well understood today, and more research is needed. It may be too early to confidently claim what exactly is going on inside them.

The next frontier: AI agents for subjective tasks
The AI agents on the market today work best for well-defined, verifiable domains such as coding. OpenAI’s Codex agent aims to help software engineers offload simple coding tasks. Meanwhile, Anthropic’s models have become particularly popular in AI coding tools like Cursor and Claude Code — these are some of the first AI agents that people are willing to pay up for.

However, general purpose AI agents like OpenAI’s ChatGPT Agent and Perplexity’s Comet struggle with many of the complex, subjective tasks people want to automate. When trying to use these tools for online shopping or finding a long-term parking spot, I’ve found the agents take longer than I’d like and make silly mistakes.

Agents are, of course, early systems that will undoubtedly improve. But researchers must first figure out how to better train the underlying models to complete tasks that are more subjective.

“Like many problems in machine learning, it’s a data problem,” said Lightman, when asked about the limitations of agents on subjective tasks. “Some of the research I’m really excited about right now is figuring out how to train on less verifiable tasks. We have some leads on how to do these things.”

Noam Brown, an OpenAI researcher who helped create the IMO model and o1, told TechCrunch that OpenAI has new general-purpose RL techniques which allow them to teach AI models skills that aren’t easily verified. This was how the company built the model which achieved a gold medal at IMO, he said.

OpenAI’s IMO model was a newer AI system that spawns multiple agents, which then simultaneously explore several ideas, and then choose the best possible answer. These types of AI models are becoming more popular; Google and xAI have recently released state-of-the-art models using this technique.

“I think these models will become more capable at math, and I think they’ll get more capable in other reasoning areas as well,” said Brown. “The progress has been incredibly fast. I don’t see any reason to think it will slow down.”

These techniques may help OpenAI’s models become more performant, gains that could show up in the company’s upcoming GPT-5 model. OpenAI hopes to assert its dominance over competitors with the launch of GPT-5, ideally offering the best AI model to power agents for developers and consumers.

But the company also wants to make its products simpler to use. El Kishky says OpenAI wants to develop AI agents that intuitively understand what users want, without requiring them to select specific settings. He says OpenAI aims to build AI systems that understand when to call up certain tools, and how long to reason for.

These ideas paint a picture of an ultimate version of ChatGPT: an agent that can do anything on the internet for you, and understand how you want it to be done. That’s a much different product than what ChatGPT is today, but the company’s research is squarely headed in this direction.

While OpenAI undoubtedly led the AI industry a few years ago, the company now faces a tranche of worthy opponents. The question is no longer just whether OpenAI can deliver its agentic future, but can the company do so before Google, Anthropic, xAI, or Meta beat them to it?"""

# 1. Define a concise prompt
prompt = textwrap.dedent("""\
Extract people's name, ai models, products and company names in order of appearance.
Use exact text for extractions. Do not paraphrase or overlap entities.
Provide meaningful related entities for each entity to add context.""")

# 2. Provide a high-quality example to guide the model
examples = [
    lx.data.ExampleData(
        text=(
            "David Ha from Sakana AI labs has trained many models"
            " including the early 'WM1' and his company makes a product called 'AI Scientist' ."
        ),
        extractions=[
            lx.data.Extraction(
                extraction_class="person_name",
                extraction_text="David Ha",
                attributes={"company": "Sakana AI"},
            ),
            lx.data.Extraction(
                extraction_class="company_name",
                extraction_text="Sakana AI",
                attributes={"employee": "David Ha"},
            ),
            lx.data.Extraction(
                extraction_class="ai_model",
                extraction_text="WM1",
                attributes={"company": "Sakana AI"},
            ),
            lx.data.Extraction(
                extraction_class="product",
                extraction_text="'AI Scientist'",
                attributes={"company": "Sakana AI"},
            ),
        ],
    )
]

# 3. Run the extraction on your input text
input_text = (
    TC_ARTICLE
)
result = lx.extract(
    text_or_documents=input_text,
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-flash",
)

for ex in result.extractions:
    if ex.extraction_class == "person_name":
        print(ex.extraction_class)
        print(ex.extraction_text)
        print(ex.attributes)
        print(ex.char_interval)
        print("====================")