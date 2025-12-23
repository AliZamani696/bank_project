FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM node:20-alpine AS production

RUN addgroup -S customgroup && adduser -S customuser -G customgroup

WORKDIR /app

COPY package*.json ./
# RUN npm install --omit=dev --registry=https://registry.npmmirror.com
RUN npm install --registry=https://registry.npmmirror.com
COPY --from=builder --chown=customuser:customgroup /app/dist ./dist

USER customuser

EXPOSE 3000

CMD ["node", "dist/index.js"]
