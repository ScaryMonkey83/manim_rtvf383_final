# manim_rtvf383_final: 
## I did a code for a class on audio and recording techniques because I have stockholm syndrome.
A multiprocessing application of manim to procedurally depict audio

### The Idea:
Find a way to artisitically depict audio procedurally.

This is a lot more ambitious than it sounds. Raw audio (WAV and AIFF etc) is stored as floating point numbers between -1 and 1. These values represent 
"speaker positions" so to speak. We need a volume- this is where convolution comes into play. Convolution uses local values of an array (such as an array generated 
by loading an AIFF file) to calculate a single value at the starting index of the locality. In this case, for any i sample, that sample convolves to an average
distance from 0. This sample is now a unitless volume. Many of the values are depressed as a result of the averaging algorithem (MSE). To ensure that the effect 
is visble, normalizing the values is necessary. This this process can be seen at lines 54-80 of manim_music.py.

At this point we have to actually define the animation we want. There should be a good balance between interest and performance. The animation library, manim, 
is cpu-bound. This means it will take a long time to render regaurdless of what we do, but the more complicated the animation the longer it will take. I
decided to keep it simple: seven pyramids, one per microphone. It is worth mentioning that this entire process will only work if each audio file being fed into
the program is exactly the same length by way of samples; this is because numpy, the linear algebra engine, expects seven arrays of equal length.

Each pyramid is defined on lines 36-69 of main.py and the sole usage is on line 123. Definition includes creating five points and linking them with lines. What 
may not seem intuitive is that at point the pyramids exist as a concept. In order to draw them to the screen, they needed to be added to the ThreeDScene. This 
happens at lines 66+67, main.py

We now have our objects of interest and our data. Manim reads main.py, specifically classmethod Video.construct (line 71 main.py) to draw the animations. In order to
make the vertex of each pyramid move, we need to tell the engine to what point we need it moved. This is done by taking the cross product of two sides of the base.
The result is a vector that points directly up from the base. Multiplying this vector by the drum reading and adding it to the vector expressing the center
of the base results in the movement of the entire pyramid. This can be seen in the function process_one (line 72 main.py)

### The Problem:
Thought Bubble: "Holy shit how does manim use a single core? It took two hours to render one second of sound."

This is where I got in way over my head.

Letting a computer run for twelve hours to render a few seconds of audio isn't reasonable when you have four days until the due date. It needed to work faster. It
definitely worked, but there was no way we are going to be able to render 89 seconds of drums like this.

There is this concept in computer science called compartmentalization or "black box coding" where you expect a certain thing to do a certain thing every certain 
time it is asked. If it fails, that certain thing is the only thing that needs to be fixed. This is fantastic when everything works, less-so in the obverse. 
When an upgrade involves a fundamental change in paradigm, it can be very difficult to determine how many things need to be changed.

### Paradigm change: Multiprocessing
Moore's law is dead. Single core processing is slow. Really slow. In order to utilize the full capability of any modern computer, written code should be written 
to run on multiple processors at the same time. Just about every computer ships with at least two processors. Mine has sixteen and right now the program only uses
one. 

In order to take advantage of this, individual scopes need to be defined in which each process can work. After all, sixteen people make a hundred sandwitches faster
than twelve people make one sandwitch. manim_music.py begins by making a temporary filesystem called tmp in the working directory. We will need this later. After 
our data is loaded, it is then chunked. Chunking is the process of breaking data into managable sizes, processing each chunk, and combining the result. Since our 
unitless volume data is too large to process with one core, we choose a standard size to chunk it. In this case, it is chunked by second. Each second contains 60
frames therefore each chunk contains 60 datapoints. The chunk is then saved as a binary file in /tmp. At the same time a shell script is written to a file
to call manim and a subdirectory is made in /tmp/media/{} for each instance of manim called simultaneously. The resulting structure is able to support limitless 
manim processes processing our chunks.

In order to pull this off, we need to allow manim to take additional arguments specifying the file that we want it to save its videos and video segments to as well
as the chunk file being used. All of this information is in /tmp but manim won't know that. This is where compartmentalization comes back. Manim is an outside 
program written in python which uses main.py as a dependancy. Because of this, the manim cli (command line interface) is accessible in main.py, but it doesn't 
provide an interface to pass the informaiton we need it to have. To solve this problem, we modify the library's cli to include fields for the filepaths we need
to pass into main.py

After all this, it still took nineteen hours to process 89 seconds of video on my sixteen core laptop and I was running out of time.

### Paradigm change: Cloud Computing
Fuck it- we are deploying it to the cloud. AWS has virtual machines with all sorts of processing power. I opted for a 48 core vm costing $1.819/hr of usage. 

Cloud computing offers some pretty unique challenges. You are literally running code on a computer that doesn't exist located hundreds of miles from you. Things
like authorization (are you allowed to be doing this, here, with that thing?), operating system (mac is so amazing- I like to be able to see what is happening 
without reading lines on lines of terminal output. Unfortunately, vms are deployed with linux <ubuntu> which runs python differently to mac), software versioning 
(depandancy conflict: your code needs 2 but the code that your code needs needs 7 and the other code that your code needs needs 1. Which one do you install? There
can only be one) and remote running (okay so its doing it. How can I tell it will keep doing it when I disconnect?) are all things that are very real and often
challenging. Virtual machines do not ship with all the software you need installed. You have to put everything that you need on it yourself.

Finally, it ran in four hours.

### Underwhelming. Why is this cool?
Because we never have to do it again. I could slightly modify the animation method Video.construct() (line 71 main.py) and make my pyramids spin. You could clone 
the project and make your pyramids sit in a heptagon. Either way, it will only take four hours to render. We could use different audio files and as long as there
are seven audio files and they are the same length the program which originally took two hours to run one second of render will take four hours to do the whole 89
seconds.
