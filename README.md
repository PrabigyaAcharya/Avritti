# आवृत्ति

## Evolutionary Music Generation

## What is it?

आवृत्ति (Āvritti, Nepali word for frequency) is an application that employs evolutionary processes through genetic algorithms to create high-quality and unique music segments. With our intuitive user interface, users can experiment with different combinations of notes and variations, enabling the generation of an almost infinite number of possibilities for creative expression. By utilizing a fitness function to assess the quality of the segment, the genetic algorithm enhances the received segment with each generation. आवृत्ति allows you to explore and enjoy rich and vibrant music in new and exciting ways.

## How do I run it on my system?

You need Python 3.9 (might not work on other versions of Python) and any browser with MIDI support to run आवृत्ति.

1. First, clone this repository onto your local machine.
2. Create a virtual environment (optional) and install all requirements listed on `requirements.txt`
3. Start the backend server (make sure it's hosted at port 8000, which is the default)

```bash
$ uvicorn main:app
```

4. Open `index.html` on a browser and start using आवृत्ति!

### I'm getting CORS error, how do I fix it?

In that case, you'll need to create a server to serve the `index.html` file. You can either do that with some extension on your IDE / text editor. (eg - VS Code has Live Server extension). Or, you can do it with a NPM module named `http-server`.

Simply run

```bash
$ npm i http-server -g
```

and run the following command in the `./frontend` directory

```bash
Avritti > frontend $ http-server
```

You should now see a link to a local server. Open it and you should be able to use आवृत्ति.

#### PS: Make sure you run `http-server` or `Live Server` extension on `./frontend` directory. If you run them on the root directory of the project, you'll end up refreshing the browser every time you generate a music. This is because the music is saved in the `./output` folder and the extension will refresh whenever there is any change.
