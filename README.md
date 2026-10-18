
# ScopeMate 🎯
### Turning vague client briefs into clear project scopes

ScopeMate is an AI assistant I'm building to help content creators, freelancers, and creative professionals understand what a client actually needs before agreeing to a project.

Sometimes, a client sends a message saying they would love to collaborate but doesn't explain the deliverables, budget, timeline, or expectations. ScopeMate aims to make these conversations easier by turning informal client messages into structured project scopes and highlighting the details that still need clarification.

This project is an experiment in fine-tuning an open-weight language model for a specific, practical use case.

## ✨ Features

- **Project identification** — identifies the likely type of project or collaboration.
- **Requirement extraction** — organizes the client's stated needs.
- **Deliverable planning** — identifies expected content or work.
- **Budget and timeline tracking** — extracts known details without inventing missing values.
- **Revision limits** — records the agreed revision limit when provided.
- **Missing information detection** — highlights details that need clarification.
- **Assumptions** — separates reasonable assumptions from confirmed information.
- **Clarifying questions** — suggests questions to ask before committing to a project.
- **Structured JSON output** — produces machine-readable results for further use.

## 💡 Example Use Case

### Input

> A local museum contacted my food and travel channel. They want to collaborate and tell stories about the harbor. They can arrange a visit and would like to cross-promote our content, but they haven't specified the deliverables, budget, or timeline.

### Expected output structure

```json
{
  "project_type": "Potential museum creator collaboration",
  "requirements": [],
  "deliverables": [],
  "budget": null,
  "timeline": null,
  "revision_limit": null,
  "missing_information": [
    "Specific collaboration concept",
    "Content format and platform",
    "Expected contributions from both parties",
    "Compensation or other exchange",
    "Production and publication schedule"
  ],
  "assumptions": [],
  "clarifying_questions": [
    "What story or activity would you like to feature?",
    "What content format and platform are you proposing?",
    "What would each party contribute?",
    "Is there a fee or another form of exchange?",
    "When would you like the content published?"
  ]
}
```

*This is an illustrative example of the intended output format, not a guarantee that every model response will match it exactly.*

## 🧠 Model and Technology

ScopeMate uses the following tools and technologies:

| Technology | Purpose |
|---|---|
| Google Gemma 4 E2B | Base language model |
| Hugging Face Transformers | Model loading and inference workflow |
| PyTorch | Model training |
| PEFT / LoRA | Parameter-efficient fine-tuning |
| TRL | Supervised fine-tuning workflow |
| BitsAndBytes | 4-bit quantization experiment |
| Google Colab | Training and testing environment |
| JSONL | Dataset format |

## 🏗️ How It Was Built

### 1. Dataset preparation

I created a small custom dataset focused on content creation briefs and creator collaborations.

The dataset contains 40 examples:

- 30 training examples
- 5 validation examples
- 5 test examples

Each example pairs an informal client brief with an expected structured JSON response.

I checked the dataset for valid JSON structure and required field types before training.

### 2. Fine-tuning

I used Google Colab and Hugging Face tools to experiment with LoRA-based fine-tuning and 4-bit quantization.

The training workflow included:

1. Loading the base model and processor.
2. Preparing the dataset and chat formatting.
3. Configuring the LoRA adapter.
4. Setting up the supervised fine-tuning process.
5. Training for three epochs.
6. Evaluating the model on the validation dataset.
7. Saving the trained adapter.

The completed run reported a final training loss of approximately **1.78** and a final validation loss of approximately **2.00**.

These are preliminary training metrics. They do not, by themselves, establish the model's real-world accuracy.

### 3. Testing and backup

I tested the trained model with client briefs and checked the generated responses.

The trained adapter and its supporting files were also backed up to Google Drive to preserve the results of the training run.

## 📁 Project Structure

The project is organized around the training data, notebook, and model artifacts.

```text
ScopeMate/
├── dataset/
│   ├── train.jsonl
│   ├── validation.jsonl
│   └── test.jsonl
├── notebooks/
│   └── scopemate-finetuning.ipynb
├── inference/
│   └── test_model.py
├── README.md
└── requirements.txt
```

*Adjust this tree to match the files actually present in your repository. Do not add empty or nonexistent files just to match the example.*

The trained adapter is saved separately. Model weights and training checkpoints can be large, so they do not necessarily need to be committed directly to GitHub.

## 🚀 Getting Started

### Requirements

- Python 3.10 or a compatible version for the selected libraries
- A supported GPU environment for practical model inference and training
- Access to the base model on Hugging Face
- Any required Hugging Face authentication or model access permissions

### Training

The training notebook is designed to run in Google Colab.

1. Open the notebook in Colab.
2. Install the required libraries.
3. Upload or load the three JSONL dataset files.
4. Configure the model, processor, quantization, and LoRA adapter.
5. Run the training and evaluation cells.
6. Save the adapter and back it up.

**Notebook:** [Add your public Colab notebook link here]

### Inference

Inference requires loading the same base model used during fine-tuning and then loading the trained adapter.

The inference code should use the compatible tokenizer or processor and chat template from the training workflow.

**Important:** The saved adapter alone is not a complete standalone language model.

## 📊 Evaluation

The initial dataset was validated structurally, and the fine-tuning run completed successfully.

The project still needs broader evaluation to establish how reliably it handles unseen client briefs.

Future evaluation will focus on:

- Valid JSON generation
- Correct extraction of stated requirements
- Avoiding invented budgets and deadlines
- Appropriate identification of missing information
- Relevance of clarifying questions
- Consistency across different client scenarios

## 🌱 Why Open-Weight AI?

Working with an open-weight model gave me the opportunity to experiment with my own dataset and fine-tuning workflow rather than relying entirely on a closed, hosted AI API.

It also helped me learn more about dataset preparation, LoRA adapters, quantization, supervised fine-tuning, inference, and evaluation.

My goal is to explore how a relatively small, task-focused AI assistant can help independent creators manage client communication more clearly.

## 🛣️ Future Improvements

- Expand the dataset with more diverse and realistic client briefs.
- Improve JSON consistency and inference reliability.
- Evaluate performance on a larger unseen test set.
- Add support for different creative industries and project types.
- Make the inference workflow easier to reproduce.
- Explore an API integration if needed in the future.

A separate frontend is not part of the current prototype.

## ⚠️ Current Limitations

- The dataset is small and intended for experimentation.
- Model outputs may be incomplete or incorrect.
- Training loss is not a substitute for task-specific evaluation.
- The model should not invent missing contract terms, budgets, or deadlines.
- Human review is recommended before using generated scopes for real client agreements.

## 🤝 Contributing

Suggestions, bug reports, dataset improvements, and evaluation examples are welcome.

If you contribute, please avoid including private client information, credentials, or confidential project briefs in the repository.


## 👩‍💻 Author

**Nilam Kumari Mahato**

- GitHub: [Nilam-Kumari-Mahato](https://github.com/Nilam-Kumari-Mahato)
- LinkedIn: [Connect on LinkedIn](https://www.linkedin.com/in/nilam-kumari-mahato-5a2710307)

---

Built as part of the Hacktoberfest Open-Source AI Challenge — Week 2: Side Hustle.
