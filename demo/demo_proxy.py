"""Demo: talk to Ollama through Kalkan with the OpenAI SDK.

1. Make sure Ollama is running (gemma3:12b pulled).
2. Terminal 1:  conda activate kalkan
                python -m kalkan.proxy
3. Terminal 2:  conda activate kalkan
                python demo/demo_proxy.py

Terminal 1's log should show only [TCKN_1], never the number itself.
10000000146 is a synthetic, checksum-valid number, not real personal data.
"""

from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:8000/v1", api_key="ollama")

response = client.chat.completions.create(
    model="gemma3:12b",
    messages=[
        {
            "role": "user",
            "content": (
                "Aşağıdaki bilgilerle iki cümlelik bir başvuru özeti yaz, kimlik numarasını "
                "olduğu gibi kullan. TC: 10000000146, Talep: kredi kartı limit artışı."
            ),
        }
    ],
)
print(response.choices[0].message.content)
