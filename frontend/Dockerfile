# Use official Node.js image as a base
FROM node:20

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install --force

# Copy the rest of the application files
COPY . .


# Build the Next.js app
RUN npm run build

# Expose the port and start the Next.js app
EXPOSE 3000
CMD ["npm", "start"]