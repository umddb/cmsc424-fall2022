# Examples of E/R Models from Previous Classes

## Neilsen Database
You are asked to design a database that would help Nielsen Media Research maintain information about TV watching habits of viewers. Construct an E/R diagram for this database.

Possible entity sets include: TV Channel, TV Series, Episode, Viewer Name etc. A viewer may watch part of one show, and part of another (this would probably be the hardest thing to model). The exact amount of time (in minutes) that a user watched a show must be somehow modeled (this doesn't have to be done explicitly, but it should be possible to extract that information from whatever data is actually stored). Make any simplifying assumptions you need to make (and state them).

Some things you need to model, and watch out for:
- The information about "when" a particular episode was aired must be modeled.
- Remember that a given episode may air at multiple times.
- Episode numbers or episode names are not unique across TV Serieses.
- The database should be able to answer the queries such as: how many viewers watched at least 50% of the Sept 5 premier of "House MD" ?  
- A viewer may watch only one show at any time.


A possible solution: Note that both started-watching and stopped-watching are multi-valued, to capture the fact that the user may switch back and forth between TV channels.

![Nielsen E/R Diagram](nielsen.jpg)

