FROM debian:12-slim

RUN DEBIAN_FRONTEND=noninteractive apt update && apt install -y pipx python3-requests
COPY ./ /etc/app_skel/
RUN useradd --add-subids-for-system --system --create-home --home-dir /app --skel /etc/app_skel/ --shell /bin/bash appuser
USER appuser
WORKDIR /app
RUN ./metadata.py > config.yaml
ENV PATH /app/.local/bin:$PATH
RUN pipx install gunicorn==21.2.0 && cat /app/requirements.txt | xargs pipx inject gunicorn
EXPOSE 8080
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
