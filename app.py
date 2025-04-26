{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "23652b99-0a6f-4a6a-b18b-0942a6c0e855",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app '__main__'\n",
      " * Debug mode: on\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.\n",
      " * Running on http://127.0.0.1:5000\n",
      "Press CTRL+C to quit\n",
      " * Restarting with watchdog (windowsapi)\n"
     ]
    },
    {
     "ename": "SystemExit",
     "evalue": "1",
     "output_type": "error",
     "traceback": [
      "An exception has occurred, use %tb to see the full traceback.\n",
      "\u001b[31mSystemExit\u001b[39m\u001b[31m:\u001b[39m 1\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\lenovo\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\IPython\\core\\interactiveshell.py:3675: UserWarning: To exit: use 'exit', 'quit', or Ctrl-D.\n",
      "  warn(\"To exit: use 'exit', 'quit', or Ctrl-D.\", stacklevel=1)\n"
     ]
    }
   ],
   "source": [
    "from flask import Flask, request, jsonify\n",
    "import pickle\n",
    "import numpy as np\n",
    "from flask_cors import CORS\n",
    "\n",
    "app = Flask(__name__)\n",
    "CORS(app)  # Allow Streamlit to access this API\n",
    "\n",
    "# Load model, scaler, and encoder\n",
    "with open(\"mental_health_model.pkl\", \"rb\") as f:\n",
    "    model = pickle.load(f)\n",
    "\n",
    "with open(\"scaler.pkl\", \"rb\") as f:\n",
    "    scaler = pickle.load(f)\n",
    "\n",
    "with open(\"label_encoder.pkl\", \"rb\") as f:\n",
    "    label_encoder = pickle.load(f)\n",
    "\n",
    "@app.route(\"/predict\", methods=[\"POST\"])\n",
    "def predict():\n",
    "    data = request.get_json()\n",
    "    try:\n",
    "        features = np.array(data[\"features\"]).reshape(1, -1)\n",
    "        scaled = scaler.transform(features)\n",
    "        prediction = model.predict(scaled)\n",
    "        mood = label_encoder.inverse_transform(prediction)\n",
    "        return jsonify({\"predicted_mood\": mood[0]})\n",
    "    except Exception as e:\n",
    "        return jsonify({\"error\": str(e)})\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    app.run(debug=True)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d668272a-0b19-4138-8ad3-be09d354ce9f",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "2f51fd87-d441-462a-957b-ad50c9a369aa",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
