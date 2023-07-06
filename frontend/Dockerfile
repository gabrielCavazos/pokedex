# Use an official Node.js runtime as the base image
FROM node:14

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the working directory
COPY package*.json ./

# Install Node.js dependencies
RUN npm install

# Copy the React app code to the working directory
COPY . .

# Build the React app for production
RUN npm run build

# Expose the port on which the React app will run
EXPOSE 3000

# Define the command to start the React app
CMD ["npm", "start"]