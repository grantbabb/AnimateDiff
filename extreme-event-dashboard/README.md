# Extreme Event Dashboard

Monorepo for a React web dashboard, AWS IaC (Terraform), ML models (floods & fires), training/inference pipelines, and time-lapse weather visualization.

## Structure

- web/ — React + Vite frontend with a TimeLapsePlayer component
- infra/cloudformation — AWS CloudFormation template for core resources
- ml/ — ML models for floods and fires
- pipelines/training — Training pipeline placeholder (Dockerfile, script)
- pipelines/inference — Inference pipeline placeholder (Dockerfile, script)

## Quickstart: Web

```bash
cd web
npm install
npm run dev
```

## Quickstart: CloudFormation

```bash
cd infra/cloudformation
aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name eed-core-dev \
  --parameter-overrides Environment=dev CreateSampleResources=true ArtifactBucketName=<UNIQUE_BUCKET_NAME> \
  --capabilities CAPABILITY_NAMED_IAM
```

## Quickstart: Training

```bash
cd pipelines/training
python train.py --task flood --output artifacts/flood_model.txt
```

## Quickstart: Inference

```bash
cd pipelines/inference
python infer.py --task flood --features '{"rainfall_mm": 5, "river_level_m": 1.2, "soil_saturation": 0.8}'
```
