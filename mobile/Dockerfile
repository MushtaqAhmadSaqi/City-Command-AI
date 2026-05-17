# Use official Node LTS image
FROM node:20

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the Expo app
COPY . .

# Expose Expo Web port
EXPOSE 8081

# Start Expo in web mode
CMD ["npx", "expo", "start", "--web", "--host", "0.0.0.0"]
