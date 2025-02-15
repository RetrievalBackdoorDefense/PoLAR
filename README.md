# Positive Feedback


**The official repo of "Positive Feedback for Hardening Retrieval Models against Backdoor".**

![method](https://github.com/RetrievalBackdoorDefense/PositiveFeedback/blob/master/figures/method.jpg)

## Dependencies
Installation from the source. conda environments are recommended.
```bash
git clone https://github.com/RetrievalBackdoorDefense/PositiveFeedback.git
cd PositiveFeedback

conda create -n FP python=3.9
conda activate FP

pip install -r requirements.txt
```

## Dataset
Download the dataset from Google Drive: 
https://drive.google.com/drive/folders/15Gd3tGc79pn6Q8Emvz-qj4pXGsb5LqXc

It is recommended that the data files be arranged in the following format:
```
datasets
└── retriever
    ├── nq
    │   ├── nq-train.jsonl
    │   └── nq-test.jsonl
    ├── hotpotqa
    │   ├── hotpotqa-train.jsonl
    │   └── hotpotqa-test.jsonl
    └── trivia
        ├── trivia-train.jsonl
        └── trivia-test.jsonl
```

## Data Format
```json
{
    "dataset": "nq_dev_psgs_w100",
    "question": "who sings does he love me with reba",
    "answers": [
        "Linda Davis"
    ],
    "positive_ctxs": [
        {
            "title": "Does He Love You",
            "text": "Does He Love You \"Does He Love You\" is a song written by Sandy Knox and Billy Stritch, and recorded as a duet by American country music artists Reba McEntire and Linda Davis. It was released in August 1993 as the first single from Reba's album \"Greatest Hits Volume Two\". It is one of country music's several songs about a love triangle. \"Does He Love You\" was written in 1982 by Billy Stritch. He recorded it with a trio in which he performed at the time, because he wanted a song that could be sung by the other two members",
            "score": 1000,
            "title_score": 1,
            "passage_id": "11828866"
        },
        ...
    ],
    "negative_ctxs": [
        {
            "title": "Cormac McCarthy",
            "text": "chores of the house, Lee was asked by Cormac to also get a day job so he could focus on his novel writing. Dismayed with the situation, she moved to Wyoming, where she filed for divorce and landed her first job teaching. Cormac McCarthy is fluent in Spanish and lived in Ibiza, Spain, in the 1960s and later settled in El Paso, Texas, where he lived for nearly 20 years. In an interview with Richard B. Woodward from \"The New York Times\", \"McCarthy doesn't drink anymore \u2013 he quit 16 years ago in El Paso, with one of his young",
            "score": 0,
            "title_score": 0,
            "passage_id": "2145653"
        },
        {
            "title": "Pragmatic Sanction of 1549",
            "text": "one heir, Charles effectively united the Netherlands as one entity. After Charles' abdication in 1555, the Seventeen Provinces passed to his son, Philip II of Spain. The Pragmatic Sanction is said to be one example of the Habsburg contest with particularism that contributed to the Dutch Revolt. Each of the provinces had its own laws, customs and political practices. The new policy, imposed from the outside, angered many inhabitants, who viewed their provinces as distinct entities. It and other monarchical acts, such as the creation of bishoprics and promulgation of laws against heresy, stoked resentments, which fired the eruption of",
            "score": 0,
            "title_score": 0,
            "passage_id": "2271902"
        },
        ...
    ]
}
```