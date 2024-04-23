# cltl-llama

Implementation of Llama for the Leolani platform. It requires a Llama server to send requests to.

## Installing a Llqama server:

https://python.langchain.com/docs/integrations/llms/llamacpp/

pip install llama-cpp-python[server]==0.2.62
pip install openai

Download the Llama file from:

https://huggingface.co/QuantFactory/Meta-Llama-3-8B-Instruct-GGUF/tree/main?source=post_page-----a563c6a47f49--------------------------------


pip install sse_starlette
pip install starlette_context
pip install pydantic_settings

#with CPU only
python -m llama_cpp.server --host 0.0.0.0 --model ./models/Meta-Llama-3-8B-Instruct.Q2_K.gguf --n_ctx 2048

#If you have a NVidia GPU
python -m llama_cpp.server --host 0.0.0.0 --model ./models/Meta-Llama-3-8B-Instruct.Q2_K.gguf --n_ctx 2048 --n_gpu_layers 28





This repository is a component of the [Leolani framework](https://github.com/leolani/cltl-combot).
For usage of the component within the framework see the instructions there.


## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- LICENSE -->
## License

Distributed under the MIT License. See [`LICENSE`](https://github.com/leolani/cltl-combot/blob/main/LICENCE) for more information.

<!-- CONTACT -->
## Authors

* [Taewoon Kim](https://tae898.github.io/)
* [Thomas Baier](https://www.linkedin.com/in/thomas-baier-05519030/)
* [Selene Báez Santamaría](https://selbaez.github.io/)
* [Piek Vossen](https://github.com/piekvossen)