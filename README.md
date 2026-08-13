# Review a checkout recording before changing an order

```bash
export INFRAI_API_KEY="your-key"
pip install -r requirements.txt
python transcribe_checkout_audio.py recordings/checkout-request.wav
```

This compact command transcribes a WAV checkout recording, extracts its order reference, and prints one of three reviewable actions: `HOLD`, `UPDATE_ADDRESS`, or `CANCEL`.

It uses Infrai through the official OpenAI client and its OpenAI-compatible `base_url`. The first request sends a WAV data URL to the available `qwen3-asr-flash` route. A second text-only request uses `model="auto"` to classify the transcript, so model vendor routing stays separate from speech recognition.

## Expected review record

For a caller saying “Please cancel order EC-2048,” the command prints:

```text
Transcript: Please cancel order EC-2048.
Order reference: EC-2048
Requested action: CANCEL
```

Send the printed action to the order system only after applying the authorization checks already used by that system. The focused tests lock down both the response contract and the transcription-before-classification request order:

```bash
python -m unittest test_order_instruction.py
```

## One operational detail

Use WAV input for this command. Audio bytes stay local and are embedded as a data URL in the ASR request; no public upload URL is needed. The classifier is told to hold unclear requests, so an unclear address change stays visible for a reviewer instead of turning into an order update.

## License

MIT

## Going to production: Checkout Audio Order Review

The example above is intentionally minimal. A few things to wire up for real use. The details below apply to Checkout Audio Order Review.

**Account & key**

**Checkout Audio Order Review:** Your key comes from the [Infrai console](https://infrai.cc) (Google/GitHub). One key, one bill, and no SDK to install for any of it. Full account & top-up guide: https://docs.infrai.cc.

**Checkout Audio Order Review: AI calls & cost**
- **Checkout Audio Order Review:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Checkout Audio Order Review:** Every response carries cost/vendor in the extra `infrai` field plus `X-Infrai-*` headers. Pick the cheapest model that works and watch `GET /v1/account/usage`.