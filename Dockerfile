from debian:12-slim

RUN DEBIAN_FRONTEND=noninteractive apt update && apt install -y pipx
COPY ./static/ ./templates/ ./app.py ./config.yaml ./requirements.txt /etc/app_skel/
RUN useradd --add-subids-for-system --system --create-home --home-dir /app --skel /etc/app_skel/ --shell /bin/bash appuser
USER appuser
RUN pipx install waitress==3.0.0 && cat /app/requirements.txt | xargs pipx inject waitress
EXPOSE 8080
ENV PATH /app/.local/bin:$PATH
CMD ["waitress-serve", "--port", "8080", "app:app"]
