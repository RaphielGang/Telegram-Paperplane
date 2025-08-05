FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
	git \
	curl \
	sudo \
	libwebp-dev \
	redis-server \
	redis-tools \
	neofetch \
	libssl-dev \
	libjpeg-dev \
	jq \
	pv \
	&& rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/src/app/bin:$PATH"
WORKDIR /usr/src/app

# Copy the current repository files
COPY . .

RUN pip install --no-cache-dir -r requirements.txt


# Create necessary directories
RUN mkdir -p bin logs

# Set proper permissions for start script
RUN chmod +x init/start.sh

# Create a non-root user for security
RUN useradd -m -u 1000 paperplane && \
    chown -R paperplane:paperplane /usr/src/app

USER paperplane

#
# Finalization
#
CMD ["bash","init/start.sh"]
