# Recognition2

## Preinstall
```
sudo apt install cmake 
```

## Create Env
```
python3 -m venv venv
. venv/bin/activate
pip install --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/nightly/cu117
```

## Start Backend server
```
uvicorn webapp:app
```