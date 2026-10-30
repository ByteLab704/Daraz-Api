FROM python:3.10-slim

# Working directory সেট করা
WORKDIR /app

# সিস্টেম ডিপেন্ডেন্সি এবং প্লে-রাইট ব্রাউজারের প্রয়োজনীয় প্যাকেজ ইনস্টল করা
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libgobject-2.0-0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    && rm -rf /var/lib/apt/lists/*

# পাইথন ডিপেন্ডেন্সি ইনস্টল করা
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Playwright এবং Chromium ব্রাউজার ইনস্টল করা
RUN playwright install chromium
RUN playwright install-deps chromium

# প্রজেক্টের বাকি ফাইলগুলো (main.py এবং অন্যান্য মডিউল) কপি করা
COPY . .

# Hugging Face-এর নিয়ম অনুযায়ী পোর্ট 7860 এক্সপোজ করা
EXPOSE 7860

# FastAPI সার্ভার স্টার্ট করার কমান্ড
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]