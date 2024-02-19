FROM python:3.10

WORKDIR /dice_and_die_api
COPY ./requirements.txt /dice_and_die_api/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /dice_and_die_api
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]