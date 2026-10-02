# Build context is city-techno-vision/ (see template.yaml Metadata.DockerContext).
FROM public.ecr.aws/lambda/python:3.12

COPY web/requirements.txt ${LAMBDA_TASK_ROOT}/requirements.txt
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt

COPY src ${LAMBDA_TASK_ROOT}/src
COPY web/lambda_handler.py ${LAMBDA_TASK_ROOT}/lambda_handler.py

ENV YOLO_MODEL_PATH=yolov8n-oiv7.pt
ENV FENCE_MODEL_ID=nvidia/segformer-b0-finetuned-cityscapes-1024-1024
# Fixed, explicit cache path: the build-time user and the Lambda runtime user
# don't share a $HOME, so relying on transformers' default ~/.cache would bake
# the weights somewhere the running function can't see and force a re-download
# (which fails without outbound internet, see below) on every cold start.
ENV HF_HOME=/opt/hf-cache
# Bake both model weights into the image at build time. Otherwise the first
# request after a cold start would need outbound internet access (github.com
# for YOLO weights, huggingface.co for the fence model), which a Lambda in a
# VPC without a NAT gateway will not have, and which just adds latency either way.
RUN python -c "from ultralytics import YOLO; YOLO('${YOLO_MODEL_PATH}')"
RUN python -c "\
from transformers import SegformerForSemanticSegmentation, SegformerImageProcessor; \
SegformerImageProcessor.from_pretrained('${FENCE_MODEL_ID}'); \
SegformerForSemanticSegmentation.from_pretrained('${FENCE_MODEL_ID}')"

CMD ["lambda_handler.handler"]
