--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0
-- Dumped by pg_dump version 17.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: acted_in; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.acted_in (
    movie_id integer NOT NULL,
    actor_id integer NOT NULL
);


ALTER TABLE public.acted_in OWNER TO postgres;

--
-- Name: actor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.actor (
    actor_id integer NOT NULL,
    actor_name text
);


ALTER TABLE public.actor OWNER TO postgres;

--
-- Name: alternative_title; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alternative_title (
    movie_id integer NOT NULL,
    title character varying(100) NOT NULL
);


ALTER TABLE public.alternative_title OWNER TO postgres;

--
-- Name: content_rating; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.content_rating (
    content_rating_id integer NOT NULL,
    content_rating text
);


ALTER TABLE public.content_rating OWNER TO postgres;

--
-- Name: country; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.country (
    country_id integer NOT NULL,
    country_short_code character varying(5),
    country_name text
);


ALTER TABLE public.country OWNER TO postgres;

--
-- Name: directed; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.directed (
    movie_id integer NOT NULL,
    director_id integer NOT NULL
);


ALTER TABLE public.directed OWNER TO postgres;

--
-- Name: director; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.director (
    director_id integer NOT NULL,
    director_name text
);


ALTER TABLE public.director OWNER TO postgres;

--
-- Name: genre; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.genre (
    genre_id integer NOT NULL,
    genre_name text
);


ALTER TABLE public.genre OWNER TO postgres;

--
-- Name: keyword; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.keyword (
    keyword_id integer NOT NULL,
    keyword text
);


ALTER TABLE public.keyword OWNER TO postgres;

--
-- Name: language; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.language (
    language_id integer NOT NULL,
    language_name text
);


ALTER TABLE public.language OWNER TO postgres;

--
-- Name: movie; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.movie (
    movie_id integer NOT NULL,
    tmdb_id integer NOT NULL,
    imdb_id text,
    title character varying(100),
    plot text,
    viewers_rating numeric(3,1),
    release_year integer,
    watchmode_id integer,
    runtime integer,
    number_of_ratings integer,
    CONSTRAINT movie_viewers_rating_check CHECK (((viewers_rating >= (0)::numeric) AND (viewers_rating <= (10)::numeric)))
);


ALTER TABLE public.movie OWNER TO postgres;

--
-- Name: movie_content_rating; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.movie_content_rating (
    movie_id integer NOT NULL,
    content_rating_id integer NOT NULL
);


ALTER TABLE public.movie_content_rating OWNER TO postgres;

--
-- Name: movie_country; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.movie_country (
    movie_id integer NOT NULL,
    country_id integer NOT NULL
);


ALTER TABLE public.movie_country OWNER TO postgres;

--
-- Name: movie_genre; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.movie_genre (
    movie_id integer NOT NULL,
    genre_id integer NOT NULL
);


ALTER TABLE public.movie_genre OWNER TO postgres;

--
-- Name: movie_keyword; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.movie_keyword (
    movie_id integer NOT NULL,
    keyword_id integer NOT NULL
);


ALTER TABLE public.movie_keyword OWNER TO postgres;

--
-- Name: movie_language; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.movie_language (
    movie_id integer NOT NULL,
    language_id integer NOT NULL
);


ALTER TABLE public.movie_language OWNER TO postgres;

--
-- Name: movie_summary; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.movie_summary AS
 SELECT m.tmdb_id,
    m.imdb_id,
    m.title,
    m.plot,
    cr.content_rating,
    m.runtime,
    ( SELECT count(*) AS count
           FROM public.movie_keyword mk
          WHERE (mk.movie_id = m.movie_id)) AS number_of_keywords,
    ( SELECT count(*) AS count
           FROM public.movie_country mc
          WHERE (mc.movie_id = m.movie_id)) AS number_of_countries
   FROM public.movie m,
    public.movie_content_rating mcr,
    public.content_rating cr
  WHERE ((m.movie_id = mcr.movie_id) AND (mcr.content_rating_id = cr.content_rating_id));


ALTER VIEW public.movie_summary OWNER TO postgres;

--
-- Data for Name: acted_in; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.acted_in (movie_id, actor_id) FROM stdin;
1	1
1	2
1	3
2	4
2	5
2	6
3	4
3	7
3	8
4	9
4	10
4	11
5	12
5	13
5	14
6	8
6	4
6	15
7	4
7	16
7	17
8	4
8	7
8	8
9	18
9	19
9	20
10	18
10	21
10	19
11	18
11	22
11	23
12	4
12	24
12	25
13	26
13	18
13	27
14	28
14	29
14	30
15	31
15	32
15	33
16	34
16	35
16	36
17	37
17	35
17	38
18	39
18	40
18	41
19	42
19	43
19	44
20	45
20	46
20	47
21	45
21	48
21	37
22	49
22	50
22	51
23	52
23	53
23	54
24	44
24	55
24	56
25	45
25	57
25	58
26	18
26	59
26	7
27	55
27	60
27	61
28	62
28	63
28	64
29	18
29	65
29	19
30	18
30	66
30	67
31	18
31	66
31	68
32	69
32	4
32	21
33	69
33	70
33	8
34	69
34	71
34	72
35	49
35	73
35	74
36	49
36	75
36	76
37	77
37	78
37	79
38	41
38	80
38	81
39	82
39	83
39	84
40	83
40	85
40	86
41	87
41	88
41	44
42	87
42	89
42	90
43	87
43	91
43	92
44	87
44	93
44	94
45	87
45	95
45	96
46	87
46	97
46	98
47	87
47	97
47	99
48	87
48	100
48	101
49	102
49	103
49	104
50	87
50	105
50	106
\.


--
-- Data for Name: actor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.actor (actor_id, actor_name) FROM stdin;
1	Marlon Brando
2	Al Pacino
3	James Caan
4	Akshay Kumar
5	Katrina Kaif
6	Nana Patekar
7	Suniel Shetty
8	Paresh Rawal
9	Song Kang-ho
10	Lee Sun-kyun
11	Cho Yeo-jeong
12	Keanu Reeves
13	Laurence Fishburne
14	Carrie-Anne Moss
15	Mithun Chakraborty
16	Vidya Balan
17	Shiney Ahuja
18	Shah Rukh Khan
19	Arjun Rampal
20	Kareena Kapoor
21	Priyanka Chopra Jonas
22	Florian Lukas
23	Om Puri
24	Fardeen Khan
25	Riteish Deshmukh
26	Preity G Zinta
27	Saif Ali Khan
28	Lubna Azabal
29	Mélissa Désormeaux-Poulin
30	Maxim Gaudette
31	Aamir Khan
32	Madhavan
33	Mona Singh
34	Harrison Ford
35	Ryan Gosling
36	Ana de Armas
37	Margot Robbie
38	Issa Rae
39	John Travolta
40	Uma Thurman
41	Samuel L. Jackson
42	Jet Li
43	Bob Hoskins
44	Morgan Freeman
45	Leonardo DiCaprio
46	Joseph Gordon-Levitt
47	Elliot Page
48	Jonah Hill
49	Will Smith
50	Thandiwe Newton
51	Jaden Smith
52	Tom Hanks
53	Robin Wright
54	Gary Sinise
55	Brad Pitt
56	Kevin Spacey
57	Kate Winslet
58	Billy Zane
59	Sushmita Sen
60	Edward Norton
61	Meat Loaf
62	Christian Bale
63	Heath Ledger
64	Aaron Eckhart
65	Deepika Padukone
66	Kajol
67	Rani Mukerji
68	Amitabh Bachchan
69	Salman Khan
70	Asin Thottumkal
71	Govinda
72	Lara Dutta
73	Eva Mendes
74	Kevin James
75	Bridget Moynahan
76	Bruce Greenwood
77	Mel Gibson
78	Helen Hunt
79	Marisa Tomei
80	Rick Gonzalez
81	Robert Ri&apos;chard
82	Michael B. Jordan
83	Sylvester Stallone
84	Tessa Thompson
85	Antonio Tarver
86	Milo Ventimiglia
87	Jim Carrey
88	Jennifer Aniston
89	Maura Tierney
90	Amanda Donohoe
91	Cameron Diaz
92	Peter Riegert
93	Courteney Cox
94	Sean Young
95	Zooey Deschanel
96	Bradley Cooper
97	Jeff Daniels
98	Lauren Holly
99	Rob Riggle
100	Renée Zellweger
101	Anthony Anderson
102	Adam Sandler
103	Kate Beckinsale
104	Christopher Walken
105	Ed Harris
106	Laura Linney
\.


--
-- Data for Name: alternative_title; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alternative_title (movie_id, title) FROM stdin;
4	Parasite
19	Unleashed
\.


--
-- Data for Name: content_rating; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.content_rating (content_rating_id, content_rating) FROM stdin;
1	R
2	Not Rated
3	N/A
4	PG-13
5	PG
\.


--
-- Data for Name: country; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.country (country_id, country_short_code, country_name) FROM stdin;
1	US	United States
2	IN	India
3	KR	South Korea
4	AU	Australia
5	DE	Germany
6	CA	Canada
7	FR	France
8	GB	United Kingdom
9	ES	Spain
10	MX	Mexico
11	JP	Japan
\.


--
-- Data for Name: directed; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.directed (movie_id, director_id) FROM stdin;
1	1
2	2
2	3
3	4
4	5
5	6
5	7
6	8
7	4
8	9
9	10
10	11
11	11
12	12
13	13
14	14
15	15
16	14
17	16
18	17
19	18
20	19
21	20
22	21
23	22
24	23
25	24
26	25
27	23
28	19
29	25
30	26
31	26
32	27
33	2
34	27
35	28
36	29
37	30
38	31
39	32
40	33
41	34
42	34
43	35
44	34
45	36
46	37
46	38
47	38
47	37
48	38
48	37
49	39
50	40
\.


--
-- Data for Name: director; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.director (director_id, director_name) FROM stdin;
1	Francis Ford Coppola
2	Anees Bazmee
3	Mayur K. Barot
4	Priyadarshan
5	Bong Joon Ho
6	Lana Wachowski
7	Lilly Wachowski
8	Umesh Shukla
9	Neeraj Vora
10	Anubhav Sinha
11	Farhan Akhtar
12	Sajid Khan
13	Nikkhil Advani
14	Denis Villeneuve
15	Rajkumar Hirani
16	Greta Gerwig
17	Quentin Tarantino
18	Louis Leterrier
19	Christopher Nolan
20	Martin Scorsese
21	Gabriele Muccino
22	Robert Zemeckis
23	David Fincher
24	James Cameron
25	Farah Khan
26	Karan Johar
27	David Dhawan
28	Andy Tennant
29	Alex Proyas
30	Nancy Meyers
31	Thomas Carter
32	Ryan Coogler
33	Sylvester Stallone
34	Tom Shadyac
35	Chuck Russell
36	Peyton Reed
37	Peter Farrelly
38	Bobby Farrelly
39	Frank Coraci
40	Peter Weir
\.


--
-- Data for Name: genre; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.genre (genre_id, genre_name) FROM stdin;
1	Crime
2	Drama
3	Comedy
4	Action
5	Thriller
6	Sci-Fi
7	Fantasy
8	Horror
9	Mystery
10	Adventure
11	Musical
12	War
13	Biography
14	Romance
15	Sport
\.


--
-- Data for Name: keyword; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.keyword (keyword_id, keyword) FROM stdin;
1	mafia
2	patriarch
3	crime family
4	organized crime
5	gangster
6	love
7	engagement
8	painter
9	acting
10	freeze frame
11	remake of malayalam film
12	wrong telephone number
13	farce
14	friendship
15	police
16	class differences
17	plot twist
18	fraud
19	social satire
20	house
21	artificial reality
22	simulated reality
23	dystopia
24	post apocalypse
25	artificial intelligence
26	reference to the bhagavad gita
27	atheist
28	satire
29	hare krishna
30	burping
31	key
32	mansion
33	superstition
34	supernatural power
35	ritual
36	money
37	swimming pool
38	robbery
39	antique
40	father son relationship
41	regeneration
42	india
43	current
44	train
45	bound and gagged
46	cleave gag
47	character name as title
48	bad guy wins
49	3d
50	3 dimensional
51	intermission
52	fistfight
53	child in jeopardy
54	shower
55	showering
56	shower scene
57	shower room
58	homosexual overtones
59	gay joke
60	neighbor
61	reverse footage
62	breaking the fourth wall
63	middle east
64	christian muslim conflict
65	pregnant from rape
66	prison
67	missing baby
68	motivation
69	coming of age
70	against the system
71	hairy chest
72	papadum
73	future noir
74	environmental damage
75	memory implant
76	detective
77	replicant
78	barbie
79	mattel
80	existential crisis
81	doll
82	voice over narration
83	nonlinear timeline
84	overdose
85	drug use
86	drug overdose
87	rape
88	dog
89	collar
90	piano duet
91	deception
92	ice cream cone
93	dream
94	ambiguous ending
95	subconscious
96	mindbender
97	surprise ending
98	based on true story
99	stockbroker
100	1990s
101	adultery
102	sex in bed
103	passion
104	hardwork
105	american dream
106	cameo appearance by real life subject
107	vietnam war
108	based on novel
109	vietnam
110	mother son relationship
111	war hero
112	serial killer
113	murder
114	murder investigation
115	severed head
116	iceberg
117	titanic
118	drowning
119	told in flashback
120	shipwreck
121	female director
122	sibling rivalry
123	female filmmaker
124	parody comedy
125	daughter
126	anti establishment
127	insomnia
128	multiple personality disorder
129	group therapy
130	psychopath
131	superhero
132	moral dilemma
133	clown
134	criminal mastermind
135	actor
136	1970s
137	mumbai india
138	2000s
139	fire
140	best friend
141	tomboy
142	principal
143	male female relationship
144	heartbreak
145	melodrama
146	marriage
147	funeral
148	wealth
149	cricket the sport
150	grandmother grandson relationship
151	letter
152	confession of love
153	woman wears eyeglasses
154	neo screwball comedy
155	runaway bride
156	coma
157	airport
158	single mother
159	wedding
160	secret
161	honeymoon
162	heiress
163	gossip
164	quitting a job
165	newspaper
166	advice
167	humanoid robot
168	man versus machine
169	prosthetic arm
170	advertising
171	telepathy
172	bare foot woman
173	heterosexuality
174	f rated
175	red panties
176	scantily clad female
177	underage drinking
178	teenager
179	gym
180	training
181	fight
182	boxing
183	boxing match
184	old age
185	ghetto
186	reminiscence
187	retired boxer
188	divine intervention
189	reference to god
190	catchphrase
191	magic
192	birthday wish
193	liar
194	lie
195	lawyer
196	los angeles california
197	alter ego
198	masked man
199	wisecrack humor
200	pet dog
201	jack russell terrier
202	nudity
203	stupidity
204	owner dog relationship
205	master dog relationship
206	breakup
207	pessimism
208	depression
209	eccentricity
210	road trip
211	toilet humor
212	briefcase full of money
213	road movie
214	sequel
215	four word title
216	toe sucking
217	cat
218	dissociative identity disorder
219	multiple personality
220	on the road
221	erection visible through clothing
222	erect penis
223	remote control
224	workaholic
225	architect
226	employer employee relationship
227	obesity
228	hidden camera
229	fictional reality show
230	controlled environment
231	paranoia
\.


--
-- Data for Name: language; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.language (language_id, language_name) FROM stdin;
1	English
2	Italian
3	Latin
4	Hindi
5	Korean
6	Bengali
7	French
8	Arabic
9	Spanish
10	Japanese
11	Cantonese
12	Swedish
13	Mandarin
14	Urdu
15	Punjabi
16	German
\.


--
-- Data for Name: movie; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.movie (movie_id, tmdb_id, imdb_id, title, plot, viewers_rating, release_year, watchmode_id, runtime, number_of_ratings) FROM stdin;
1	238	tt0068646	The Godfather	The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.	9.2	1972	\N	175	2057473
2	20294	tt0488798	Welcome	A man falls in love with a beautiful woman, but later discovers that her brothers are gangsters.	7.1	2007	\N	150	26255
3	21614	tt0242519	Hera Pheri	Two tenants and a landlord look for answers to all their money problems - but when their opportunity arrives, will they know what to do with it?	8.2	2000	\N	156	73988
4	496243	tt6751668	Gisaengchung	Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.	8.5	2019	\N	132	999122
5	603	tt0133093	The Matrix	When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth--the life he knows is the elaborate deception of an evil cyber-intelligence.	8.7	1999	\N	136	2095617
6	135718	tt2283748	OMG: Oh My God!	A shopkeeper takes God to court when his shop is destroyed by an earthquake.	8.1	2012	\N	125	66637
7	19025	tt0995031	Bhool Bhulaiyaa	An NRI and his wife decide to stay in his ancestral home, paying no heed to the warnings about ghosts. Soon, inexplicable occurrences cause him to call a psychiatrist to help solve the mystery.	7.5	2007	\N	159	33410
8	20359	tt0419058	Phir Hera Pheri	A twist of fate changes the lives of Raju, Shyam and Baburao when they get cheated by a fraudster. They must now find a way to repay a loan taken from a dreaded gangster.	7.3	2006	\N	153	28756
9	41517	tt1562871	Ra.One	When the titular antagonist of an action game takes on physical form, it&apos;s only the game&apos;s less powerful protagonist who can save his creator&apos;s family.	4.9	2011	\N	156	47601
10	17501	tt0461936	Don	Vijay is recruited by a police officer to masquerade as his lookalike Don, the leader of an international gang of smugglers. Things go wrong when the officer is killed and Vijay is left to fend for himself.	7.1	2006	\N	171	41642
11	41109	tt1285241	Don 2	Don turns himself in and escapes with Vardhaan from prison, following which he recruits a team to steal currency printing plates from a bank in Berlin.	7.1	2011	\N	148	59081
12	4157	tt0806088	Heyy Babyy	Three bachelors who are compulsive womanizers find their lives turned upside down when a baby is left at their doorstep. The trio suspect each other of being the father.	6.1	2007	\N	144	16243
13	4254	tt0347304	Kal Ho Naa Ho	Naina, an introverted, perpetually depressed girl&apos;s life changes when she meets Aman. But Aman has a secret of his own which changes their lives forever. Embroiled in all this is Rohit, Naina&apos;s best friend who conceals his love fo...	7.9	2003	\N	186	76616
14	46738	tt1255953	Incendies	Twins journey to the Middle East to discover their family history and fulfill their mother&apos;s last wishes.	8.3	2010	\N	131	211797
15	20453	tt1187043	3 Idiots	Two friends are searching for their long lost companion. They revisit their college days and recall the memories of their friend who inspired them to think differently, even as the rest of the world called them &quot;idiots&quot;.	8.4	2009	\N	170	445432
16	335984	tt1856101	Blade Runner 2049	Young Blade Runner K&apos;s discovery of a long-buried secret leads him to track down former Blade Runner Rick Deckard, who&apos;s been missing for thirty years.	8.0	2017	\N	164	686625
17	346698	tt1517268	Barbie	Barbie and Ken are having the time of their lives in the colorful and seemingly perfect world of Barbie Land. However, when they get a chance to go to the real world, they soon discover the joys and perils of living among humans.	6.8	2023	\N	114	571413
18	680	tt0110912	Pulp Fiction	The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.	8.9	1994	\N	154	2266472
19	10027	tt0342258	Danny the Dog	A man enslaved by the mob since childhood and raised into behaving like a human attack dog escapes his captors and attempts to start a new life.	7.0	2005	\N	103	108912
20	27205	tt1375666	Inception	A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O., but his tragic past may doom the project and his team to disaster.	8.8	2010	1182444	148	2602766
21	106646	tt0993846	The Wolf of Wall Street	Based on the true story of Jordan Belfort, from his rise to a wealthy stock-broker living the high life to his fall involving crime, corruption and the federal government.	8.2	2013	\N	180	1629645
22	1402	tt0454921	The Pursuit of Happyness	A struggling salesman takes custody of his son as he&apos;s poised to begin a life-changing professional career.	8.0	2006	\N	117	574267
23	13	tt0109830	Forrest Gump	The history of the United States from the 1950s to the &apos;70s unfolds from the perspective of an Alabama man with an IQ of 75, who yearns to be reunited with his childhood sweetheart.	8.8	1994	\N	142	2314429
24	807	tt0114369	Se7en	Two detectives, a rookie and a veteran, hunt a serial killer who uses the seven deadly sins as his motives.	8.6	1995	\N	127	1842793
25	597	tt0120338	Titanic	A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.	7.9	1997	\N	194	1308495
26	14134	tt0347473	Main Hoon Na	An army major goes undercover as a college student. His mission is both professional and personal: to protect his general&apos;s daughter from a radical militant, and to find his estranged half-brother.	7.1	2004	\N	182	41172
27	550	tt0137523	Fight Club	An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into much more.	8.8	1999	\N	139	2383262
28	155	tt0468569	The Dark Knight	When a menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman, James Gordon and Harvey Dent must work together to put an end to the madness.	9.0	2008	\N	152	2932729
29	8079	tt1024943	Om Shanti Om	In the 1970s, Om, an aspiring actor, is murdered, but is immediately reincarnated into the present day. He attempts to discover the mystery of his demise and find Shanti, the love of his previous life.	6.8	2007	\N	162	50911
30	11854	tt0172684	Kuch Kuch Hota Hai	During their college years, Anjali was in love with her best-friend Rahul, but he had eyes only for Tina. Years later, Rahul and the now-deceased Tina&apos;s eight-year-old daughter attempts to reunite her father and Anjali.	7.5	1998	\N	185	58306
31	10757	tt0248126	Kabhi Khushi Kabhie Gham...	After marrying a poor woman, rich Rahul is disowned by his father and moves to London to build a new life. Years later, his now-grown younger brother Rohan embarks on a mission to bring Rahul back home and reunite the family.	7.4	2001	\N	210	57955
32	20495	tt0418362	Mujhse Shaadi Karogi	Sameer, fast at losing his temper is re-located to Goa where he falls in love with Rani. But Sameer&apos;s new roommate Sunny, has some plans of his own.	6.7	2004	\N	163	17362
33	65946	tt1708532	Ready	Set in Thailand and India, a case of mistaken identity leads to love, and a man and his family concoct a grand scheme to win over the hearts of a woman and her greedy, conniving uncles.	4.9	2011	\N	145	20101
34	27298	tt0807758	Partner	A &apos;Love Guru&apos; assists other males, woos a widowed single mother, but becomes embroiled in controversies.	5.8	2007	\N	155	13894
35	8488	tt0386588	Hitch	A smooth-talking man falls for a hardened columnist while helping a shy accountant woo a beautiful heiress.	6.6	2005	1166745	118	338985
36	2048	tt0343818	I, Robot	In 2035, a technophobic cop investigates a crime that may have been perpetrated by a robot, which leads to a larger threat to humanity.	7.1	2004	\N	115	585654
37	3981	tt0207201	What Women Want	A cocky, chauvinistic advertising executive magically acquires the ability to hear what women are thinking.	6.5	2000	1465680	127	226275
38	7214	tt0393162	Coach Carter	Controversy surrounds high school basketball coach Ken Carter after he benches his entire team for breaking their academic contract with him.	7.3	2005	178331	136	175726
39	312221	tt3076658	Creed	The former World Heavyweight Champion Rocky Balboa serves as a trainer and mentor to Adonis Johnson, the son of his late friend and former rival Apollo Creed.	7.6	2015	\N	133	315861
40	1246	tt0479143	Rocky Balboa	Thirty years after the ring of the first bell, Rocky Balboa comes out of retirement and dons his gloves for his final fight against the reigning heavyweight champ Mason &apos;The Line&apos; Dixon.	7.1	2006	\N	102	234434
41	310	tt0315327	Bruce Almighty	A whiny news reporter is given the chance to step into God&apos;s shoes.	6.8	2003	\N	101	441119
42	1624	tt0119528	Liar Liar	A pathological liar-lawyer finds his career turned upside down when he inexplicably cannot physically lie for 24 whole hours.	6.9	1997	\N	86	340302
43	854	tt0110475	The Mask	Bank clerk Stanley Ipkiss is transformed into a manic superhero when he wears a mysterious mask.	7.0	1994	\N	101	433143
44	3049	tt0109040	Ace Ventura: Pet Detective	A goofy detective specializing in animals goes in search of the missing mascot of the Miami Dolphins.	6.9	1994	\N	86	331275
45	10201	tt1068680	Yes Man	A man challenges himself to say &quot;yes&quot; to everything.	6.8	2008	\N	104	387755
46	8467	tt0109686	Dumb and Dumber	After a woman leaves a briefcase at the airport terminal, a dumb limo driver and his dumber friend set out on a hilarious cross-country road trip to Aspen to return it.	7.3	1994	\N	107	419736
47	100042	tt2096672	Dumb and Dumber To	20 years since their first adventure, Lloyd and Harry go on a road trip to find Harry&apos;s newly discovered daughter, who was given up for adoption.	5.6	2014	\N	109	147265
48	2123	tt0183505	Me, Myself &amp; Irene	A nice-guy cop with Dissociative Identity Disorder must protect a woman on the run from a corrupt ex-boyfriend and his associates.	6.6	2000	\N	116	254472
49	9339	tt0389860	Click	A workaholic architect finds a universal remote that allows him to fast-forward and rewind to different parts of his life. Complications arise when the remote starts to overrule his choices.	6.4	2006	\N	107	364036
50	37165	tt0120382	The Truman Show	An insurance salesman discovers his whole life is actually a reality TV show.	8.2	1998	1424513	103	1234214
\.


--
-- Data for Name: movie_content_rating; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.movie_content_rating (movie_id, content_rating_id) FROM stdin;
1	1
2	2
3	2
4	1
5	1
6	2
7	2
8	3
9	2
10	2
11	2
12	2
13	2
14	1
15	4
16	1
17	4
18	1
19	1
20	4
21	1
22	4
23	4
24	1
25	4
26	2
27	1
28	4
29	2
30	2
31	2
32	3
33	2
34	2
35	4
36	4
37	4
38	4
39	4
40	5
41	4
42	4
43	4
44	4
45	4
46	4
47	4
48	1
49	4
50	5
\.


--
-- Data for Name: movie_country; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.movie_country (movie_id, country_id) FROM stdin;
1	1
2	2
3	2
4	3
5	1
5	4
6	2
7	2
8	2
9	2
9	1
10	2
11	2
11	5
12	2
13	2
13	6
14	6
14	7
15	2
16	1
16	8
16	6
16	9
17	1
17	8
18	1
19	8
19	7
19	1
20	1
20	8
21	1
22	1
23	1
24	1
25	1
25	10
26	2
27	5
27	1
28	1
28	8
29	2
30	2
31	2
31	8
32	2
33	2
34	2
35	1
36	1
36	5
37	1
38	1
38	5
39	1
40	1
41	1
42	1
43	1
44	1
45	1
45	8
46	1
47	1
47	11
48	1
49	1
50	1
\.


--
-- Data for Name: movie_genre; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.movie_genre (movie_id, genre_id) FROM stdin;
1	1
1	2
2	3
2	1
2	2
3	4
3	3
3	1
4	2
4	5
5	4
5	6
6	3
6	2
6	7
7	3
7	8
7	9
8	3
8	1
9	4
9	10
9	6
10	4
10	1
10	5
11	4
11	1
11	5
12	3
12	2
13	3
13	2
13	11
14	2
14	9
14	12
15	3
15	2
16	4
16	2
16	9
17	10
17	3
17	7
18	1
18	2
19	4
19	1
19	5
20	4
20	10
20	6
21	13
21	3
21	1
22	13
22	2
23	2
23	14
24	1
24	2
24	9
25	2
25	14
26	4
26	3
26	2
27	2
28	4
28	1
28	2
29	4
29	3
29	2
30	3
30	2
30	11
31	2
31	11
31	14
32	3
32	14
33	4
33	3
33	14
34	3
34	2
34	14
35	3
35	14
36	4
36	9
36	6
37	3
37	7
37	14
38	13
38	2
38	15
39	4
39	2
39	15
40	4
40	2
40	15
41	3
41	7
42	3
42	7
43	4
43	3
43	1
44	3
45	3
45	14
46	3
47	3
48	3
49	3
49	2
49	7
50	3
50	2
\.


--
-- Data for Name: movie_keyword; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.movie_keyword (movie_id, keyword_id) FROM stdin;
1	1
1	2
1	3
1	4
1	5
2	6
2	7
2	8
2	9
2	10
3	11
3	12
3	13
3	14
3	15
4	16
4	17
4	18
4	19
4	20
5	21
5	22
5	23
5	24
5	25
6	26
6	27
6	28
6	29
6	30
7	31
7	32
7	33
7	34
7	35
8	36
8	37
8	38
8	5
8	39
9	40
9	41
9	42
9	43
9	44
10	45
10	46
10	47
10	48
10	15
11	48
11	49
11	50
11	51
11	52
12	53
12	54
12	55
12	56
12	57
13	58
13	59
13	60
13	61
13	62
14	63
14	64
14	65
14	66
14	67
15	68
15	69
15	70
15	71
15	72
16	73
16	74
16	75
16	76
16	77
17	78
17	79
17	80
17	81
17	82
18	83
18	84
18	85
18	86
18	87
19	88
19	89
19	90
19	91
19	92
20	93
20	94
20	95
20	96
20	97
21	98
21	99
21	100
21	101
21	102
22	103
22	104
22	29
22	105
22	106
23	107
23	108
23	109
23	110
23	111
24	112
24	76
24	113
24	114
24	115
25	116
25	117
25	118
25	119
25	120
26	121
26	122
26	123
26	124
26	125
27	97
27	126
27	127
27	128
27	129
28	130
28	131
28	132
28	133
28	134
29	135
29	136
29	137
29	138
29	139
30	140
30	141
30	142
30	143
30	144
31	6
31	145
31	146
31	147
31	148
32	149
32	150
32	151
32	152
32	153
33	154
33	155
33	156
33	157
33	6
34	158
34	159
34	160
34	161
34	162
35	163
35	164
35	165
35	14
35	166
36	167
36	168
36	25
36	23
36	169
37	170
37	171
37	172
37	173
37	174
38	175
38	176
38	177
38	178
38	158
39	179
39	180
39	181
39	182
39	183
40	184
40	185
40	186
40	182
40	187
41	34
41	188
41	189
41	190
41	191
42	192
42	193
42	194
42	195
42	196
43	197
43	198
43	199
43	200
43	201
44	202
44	203
44	76
44	204
44	205
45	196
45	206
45	207
45	208
45	209
46	210
46	203
46	211
46	212
46	213
47	14
47	214
47	215
47	216
47	217
48	218
48	219
48	220
48	221
48	222
49	223
49	224
49	225
49	226
49	227
50	228
50	22
50	229
50	230
50	231
\.


--
-- Data for Name: movie_language; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.movie_language (movie_id, language_id) FROM stdin;
1	1
1	2
1	3
2	4
3	4
4	5
4	1
5	1
6	4
7	4
7	6
8	4
9	4
10	4
11	4
12	4
13	4
13	1
14	7
14	8
14	1
15	4
15	1
16	1
17	1
17	9
18	1
18	9
18	7
19	1
20	1
20	10
20	7
21	1
21	7
22	1
22	11
23	1
24	1
25	1
25	12
25	2
25	7
26	4
27	1
28	1
28	13
29	4
29	14
30	4
31	4
31	1
31	15
31	14
32	4
33	4
33	1
34	4
35	1
36	1
37	1
38	1
39	1
39	9
40	1
40	9
41	1
41	9
42	1
43	1
43	12
44	1
45	1
45	5
46	1
46	12
46	16
47	1
47	11
48	1
48	16
49	1
49	9
49	10
50	1
\.


--
-- Name: acted_in acted_in_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acted_in
    ADD CONSTRAINT acted_in_pkey PRIMARY KEY (movie_id, actor_id);


--
-- Name: actor actor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actor
    ADD CONSTRAINT actor_pkey PRIMARY KEY (actor_id);


--
-- Name: alternative_title alternative_title_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alternative_title
    ADD CONSTRAINT alternative_title_pkey PRIMARY KEY (movie_id, title);


--
-- Name: content_rating content_rating_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.content_rating
    ADD CONSTRAINT content_rating_pkey PRIMARY KEY (content_rating_id);


--
-- Name: country country_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.country
    ADD CONSTRAINT country_pkey PRIMARY KEY (country_id);


--
-- Name: directed directed_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.directed
    ADD CONSTRAINT directed_pkey PRIMARY KEY (movie_id, director_id);


--
-- Name: director director_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.director
    ADD CONSTRAINT director_pkey PRIMARY KEY (director_id);


--
-- Name: genre genre_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.genre
    ADD CONSTRAINT genre_pkey PRIMARY KEY (genre_id);


--
-- Name: keyword keyword_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.keyword
    ADD CONSTRAINT keyword_pkey PRIMARY KEY (keyword_id);


--
-- Name: language language_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.language
    ADD CONSTRAINT language_pkey PRIMARY KEY (language_id);


--
-- Name: movie_content_rating movie_content_rating_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movie_content_rating
    ADD CONSTRAINT movie_content_rating_pkey PRIMARY KEY (movie_id, content_rating_id);


--
-- Name: movie_country movie_country_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movie_country
    ADD CONSTRAINT movie_country_pkey PRIMARY KEY (movie_id, country_id);


--
-- Name: movie_genre movie_genre_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movie_genre
    ADD CONSTRAINT movie_genre_pkey PRIMARY KEY (movie_id, genre_id);


--
-- Name: movie movie_imdb_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movie
    ADD CONSTRAINT movie_imdb_id_key UNIQUE (imdb_id);


--
-- Name: movie_keyword movie_keyword_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movie_keyword
    ADD CONSTRAINT movie_keyword_pkey PRIMARY KEY (movie_id, keyword_id);


--
-- Name: movie_language movie_language_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movie_language
    ADD CONSTRAINT movie_language_pkey PRIMARY KEY (movie_id, language_id);


--
-- Name: movie movie_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movie
    ADD CONSTRAINT movie_pkey PRIMARY KEY (movie_id);


--
-- Name: movie movie_tmdb_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movie
    ADD CONSTRAINT movie_tmdb_id_key UNIQUE (tmdb_id);


--
-- Name: acted_in acted_in_actor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.acted_in
    ADD CONSTRAINT acted_in_actor_id_fkey FOREIGN KEY (actor_id) REFERENCES public.actor(actor_id) ON DELETE CASCADE;


--
-- Name: directed directed_director_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.directed
    ADD CONSTRAINT directed_director_id_fkey FOREIGN KEY (director_id) REFERENCES public.director(director_id) ON DELETE CASCADE;


--
-- Name: movie_content_rating movie_content_rating_content_rating_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movie_content_rating
    ADD CONSTRAINT movie_content_rating_content_rating_id_fkey FOREIGN KEY (content_rating_id) REFERENCES public.content_rating(content_rating_id) ON DELETE CASCADE;


--
-- Name: movie_country movie_country_country_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movie_country
    ADD CONSTRAINT movie_country_country_id_fkey FOREIGN KEY (country_id) REFERENCES public.country(country_id) ON DELETE CASCADE;


--
-- Name: movie_genre movie_genre_genre_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movie_genre
    ADD CONSTRAINT movie_genre_genre_id_fkey FOREIGN KEY (genre_id) REFERENCES public.genre(genre_id) ON DELETE CASCADE;


--
-- Name: movie_keyword movie_keyword_keyword_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movie_keyword
    ADD CONSTRAINT movie_keyword_keyword_id_fkey FOREIGN KEY (keyword_id) REFERENCES public.keyword(keyword_id) ON DELETE CASCADE;


--
-- Name: movie_language movie_language_language_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movie_language
    ADD CONSTRAINT movie_language_language_id_fkey FOREIGN KEY (language_id) REFERENCES public.language(language_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

