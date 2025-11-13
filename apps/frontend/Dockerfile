FROM node:22-alpine AS builder
WORKDIR /workspace
RUN corepack enable && corepack prepare pnpm@9.12.2 --activate
COPY . .
RUN pnpm install --frozen-lockfile
RUN pnpm exec nx run frontend:build

FROM nginx:alpine
COPY --from=builder /workspace/dist/apps/frontend /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
