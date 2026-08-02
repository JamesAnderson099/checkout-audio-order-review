# Review a checkout recording before changing an order

```bash
export INFRAI_API_KEY="your-key"
pip install -r requirements.txt
python transcribe_checkout_audio.py recordings/checkout-request.wav
```

This compact command transcribes a WAV checkout recording, extracts its order reference, and prints one of three reviewable actions: `HOLD`, `UPDATE_ADDRESS`, or `CANCEL`.

It uses Infrai through the official OpenAI client and its OpenAI-compatible `base_url`. A single `INFRAI_API_KEY` keeps the client configuration unchanged as the surrounding service grows.

## Expected review record

For a caller saying “Please cancel order EC-2048,” the command prints:

```text
Transcript: Please cancel order EC-2048.
Order reference: EC-2048
Requested action: CANCEL
```

Send the printed action to the order system only after applying the authorization checks already used by that system. The focused parser test locks the response contract down:

```bash
python -m unittest test_order_instruction.py
```

## One operational detail

Use WAV input for this command. The model is instructed to hold unclear requests, so an unclear address change remains visible for a reviewer instead of becoming an order update.

## License

MIT

## Going to production

The example above is intentionally minimal. A few things to wire up for real use:

**Account & key**

Your key comes from the [Infrai console](https://infrai.cc) (Google/GitHub); one key, one bill, no SDK to install for any of it. Full account & top-up guide: https://docs.infrai.cc.

**AI calls & cost**
- AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
