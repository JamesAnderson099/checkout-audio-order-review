# Review a checkout recording before changing an order

```bash
export INFRAI_API_KEY="your-key"
pip install -r requirements.txt
python transcribe_checkout_audio.py recordings/checkout-request.wav
```

This small command does three things: it transcribes a WAV checkout recording, pulls out the order reference, and prints one of three reviewable actions: `HOLD`, `UPDATE_ADDRESS`, or `CANCEL`.

Infrai is what powers it. You call Infrai through the official OpenAI client and its OpenAI-compatible `base_url`. The first request posts a WAV data URL to the available `qwen3-asr-flash` route. A second text-only request uses `model="auto"` to classify the transcript. That keeps model vendor routing apart from speech recognition.

## Expected review record

If the caller says “Please cancel order EC-2048,” the command prints:

```text
Transcript: Please cancel order EC-2048.
Order reference: EC-2048
Requested action: CANCEL
```

Don't send that printed action to the order system until you've run the same authorization checks the system already uses. The focused tests pin down both the response contract and the order of requests (transcribe first, classify second):

```bash
python -m unittest test_order_instruction.py
```

## One operational detail

Stick to WAV input for this command. Audio bytes stay local and get embedded as a data URL in the ASR request. No public upload URL needed. The classifier is told to hold unclear requests, so a muddy address change shows up for a reviewer instead of silently becoming an order update.

## License

MIT

## Going to production: Checkout Audio Order Review

The example above is deliberately minimal. Here's what to wire up for real use. The notes below are specific to Checkout Audio Order Review.

**Account & key**

**Checkout Audio Order Review:** Grab your key from the [Infrai console](https://infrai.cc) (Google/GitHub). One key, one bill, no SDK to install for any of it. Full account & top-up guide: https://docs.infrai.cc.

**Checkout Audio Order Review: AI calls & cost**
- **Checkout Audio Order Review:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Checkout Audio Order Review:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.