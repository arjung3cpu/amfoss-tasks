import { useEffect, useState } from "react";
import {
  Search,
  Heart,
  Film,
  X,
  Clock,
  Star,
  Play,
} from "lucide-react";
import "./App.css";

const API_KEY = import.meta.env.VITE_TMDB_API_KEY;
const API_URL = "https://api.themoviedb.org/3";
const IMAGE_URL = "https://image.tmdb.org/t/p/w500";

function App() {
  const [movies, setMovies] = useState([]);
  const [watchlist, setWatchlist] = useState(() => {
    try {
      return JSON.parse(
        localStorage.getItem("ohara-watchlist")
      ) || [];
    } catch {
      return [];
    }
  });

  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(false);
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [showWatchlist, setShowWatchlist] = useState(false);

  useEffect(() => {
    localStorage.setItem(
      "ohara-watchlist",
      JSON.stringify(watchlist)
    );
  }, [watchlist]);

  useEffect(() => {
    fetchMovies("popular");
  }, []);

  async function fetchMovies(query) {
    setLoading(true);

    try {
      const endpoint =
        query === "popular"
          ? `${API_URL}/movie/popular?api_key=${API_KEY}&language=en-US&page=1`
          : `${API_URL}/search/movie?api_key=${API_KEY}&language=en-US&query=${encodeURIComponent(
              query
            )}&page=1`;

      const response = await fetch(endpoint);

      if (!response.ok) {
        throw new Error("TMDB request failed");
      }

      const data = await response.json();

      setMovies(data.results || []);
    } catch (error) {
      console.error("TMDB Error:", error);
      setMovies([]);
    } finally {
      setLoading(false);
    }
  }

  function handleSearch(event) {
    event.preventDefault();

    const query = search.trim();

    if (query) {
      setShowWatchlist(false);
      fetchMovies(query);
    } else {
      fetchMovies("popular");
    }
  }

  function toggleWatchlist(movie) {
    setWatchlist((current) => {
      const exists = current.some(
        (item) => item.id === movie.id
      );

      if (exists) {
        return current.filter(
          (item) => item.id !== movie.id
        );
      }

      return [...current, movie];
    });
  }

  function isInWatchlist(movieId) {
    return watchlist.some(
      (movie) => movie.id === movieId
    );
  }

  const displayedMovies = showWatchlist
    ? watchlist
    : movies;

  return (
    <div className="app">

      {/* NAVIGATION */}

      <header className="navbar">
        <div className="logo">
          <div className="logo-icon">
            <Film size={22} />
          </div>

          <div>
            <h1>OHARA</h1>
            <span>THE CINEMATIC ARCHIVE</span>
          </div>
        </div>

        <button
          className="watchlist-button"
          onClick={() =>
            setShowWatchlist(!showWatchlist)
          }
        >
          <Heart
            size={18}
            fill={
              showWatchlist
                ? "currentColor"
                : "none"
            }
          />

          Watchlist

          <span>{watchlist.length}</span>
        </button>
      </header>


      {/* HERO */}

      <main>
        <section className="hero">
          <div className="hero-content">

            <p className="eyebrow">
              THE LIBRARY OF CINEMA
            </p>

            <h2>
              Discover stories.
              <br />
              <span>Preserve memories.</span>
            </h2>

            <p className="hero-description">
              Explore an ever-growing archive of films,
              discover hidden masterpieces, and curate
              your own personal collection.
            </p>

            <form
              className="search-box"
              onSubmit={handleSearch}
            >
              <Search size={21} />

              <input
                type="text"
                placeholder="Search for a movie..."
                value={search}
                onChange={(event) =>
                  setSearch(event.target.value)
                }
              />

              <button type="submit">
                Search
              </button>
            </form>

          </div>
        </section>


        {/* MOVIE ARCHIVE */}

        <section className="content">

          <div className="section-heading">

            <div>
              <p className="eyebrow">
                {showWatchlist
                  ? "YOUR COLLECTION"
                  : "EXPLORE THE ARCHIVE"}
              </p>

              <h3>
                {showWatchlist
                  ? "My Watchlist"
                  : "Popular Movies"}
              </h3>
            </div>

            {showWatchlist && (
              <button
                className="clear-button"
                onClick={() =>
                  setShowWatchlist(false)
                }
              >
                <X size={16} />
                Back to archive
              </button>
            )}

          </div>


          {/* LOADING */}

          {loading ? (
            <div className="loading">
              <div className="loader"></div>

              <p>
                Searching the archive...
              </p>
            </div>
          ) : displayedMovies.length === 0 ? (

            /* EMPTY STATE */

            <div className="empty">

              <Film size={42} />

              <h3>
                {showWatchlist
                  ? "Your archive is empty"
                  : "No movies found"}
              </h3>

              <p>
                {showWatchlist
                  ? "Add movies to your watchlist to see them here."
                  : "Try searching for another movie."}
              </p>

            </div>

          ) : (

            /* MOVIE GRID */

            <div className="movie-grid">

              {displayedMovies.map((movie) => (

                <MovieCard
                  key={movie.id}
                  movie={movie}
                  inWatchlist={isInWatchlist(
                    movie.id
                  )}
                  onToggle={() =>
                    toggleWatchlist(movie)
                  }
                  onOpen={() =>
                    setSelectedMovie(movie)
                  }
                />

              ))}

            </div>
          )}

        </section>

      </main>


      {/* FOOTER */}

      <footer>

        <div className="footer-logo">
          <Film size={18} />
          OHARA ARCHIVE
        </div>

        <p>
          Movie data provided by TMDB
        </p>

      </footer>


      {/* MOVIE DETAILS MODAL */}

      {selectedMovie && (
        <MovieModal
          movie={selectedMovie}
          inWatchlist={isInWatchlist(
            selectedMovie.id
          )}
          onToggle={() =>
            toggleWatchlist(selectedMovie)
          }
          onClose={() =>
            setSelectedMovie(null)
          }
        />
      )}

    </div>
  );
}


/* =========================================
   MOVIE CARD
========================================= */

function MovieCard({
  movie,
  inWatchlist,
  onToggle,
  onOpen,
}) {

  const poster = movie.poster_path
    ? `${IMAGE_URL}${movie.poster_path}`
    : null;

  return (
    <article className="movie-card">

      <div
        className="poster-container"
        onClick={onOpen}
      >

        {poster ? (

          <img
            src={poster}
            alt={movie.title}
          />

        ) : (

          <div className="no-poster">

            <Film size={35} />

            <span>
              No poster
            </span>

          </div>
        )}


        <div className="poster-overlay">

          <button className="details-button">

            <Play
              size={16}
              fill="currentColor"
            />

            View details

          </button>

        </div>


        <button
          className={`heart-button ${
            inWatchlist ? "active" : ""
          }`}
          onClick={(event) => {

            event.stopPropagation();

            onToggle();

          }}
          aria-label={
            inWatchlist
              ? "Remove from watchlist"
              : "Add to watchlist"
          }
        >

          <Heart
            size={19}
            fill={
              inWatchlist
                ? "currentColor"
                : "none"
            }
          />

        </button>

      </div>


      <div className="movie-info">

        <h4>
          {movie.title}
        </h4>

        <div className="movie-meta">

          <span>
            <Clock size={14} />

            {movie.release_date
              ? movie.release_date.slice(0, 4)
              : "N/A"}
          </span>

          <span>
            <Star
              size={14}
              fill="currentColor"
            />

            {movie.vote_average
              ? movie.vote_average.toFixed(1)
              : "N/A"}
          </span>

        </div>

      </div>

    </article>
  );
}


/* =========================================
   MOVIE DETAILS MODAL
========================================= */

function MovieModal({
  movie,
  inWatchlist,
  onToggle,
  onClose,
}) {

  const [details, setDetails] =
    useState(movie);

  const [loading, setLoading] =
    useState(true);


  useEffect(() => {

    async function fetchDetails() {

      setLoading(true);

      try {

        const response = await fetch(
          `${API_URL}/movie/${movie.id}?api_key=${API_KEY}&language=en-US`
        );

        if (!response.ok) {
          throw new Error(
            "Failed to load movie details"
          );
        }

        const data =
          await response.json();

        setDetails(data);

      } catch (error) {

        console.error(
          "Movie details error:",
          error
        );

      } finally {

        setLoading(false);

      }
    }

    fetchDetails();

  }, [movie.id]);


  const poster = details.poster_path
    ? `${IMAGE_URL}${details.poster_path}`
    : null;


  const runtime = details.runtime
    ? `${Math.floor(
        details.runtime / 60
      )}h ${
        details.runtime % 60
      }m`
    : "N/A";


  return (
    <div
      className="modal-backdrop"
      onClick={onClose}
    >

      <div
        className="modal"
        onClick={(event) =>
          event.stopPropagation()
        }
      >

        <button
          className="modal-close"
          onClick={onClose}
          aria-label="Close"
        >
          <X size={22} />
        </button>


        {poster && (
          <img
            className="modal-poster"
            src={poster}
            alt={details.title}
          />
        )}


        <div className="modal-content">

          {loading ? (

            <div className="loading modal-loading">

              <div className="loader"></div>

              <p>
                Opening archive record...
              </p>

            </div>

          ) : (

            <>

              <p className="eyebrow">
                ARCHIVE RECORD
              </p>

              <h2>
                {details.title}
              </h2>


              {details.tagline && (

                <p className="tagline">
                  “{details.tagline}”
                </p>

              )}


              <div className="modal-meta">

                <span>
                  📅{" "}
                  {details.release_date ||
                    "Unknown"}
                </span>

                <span>
                  ⭐{" "}
                  {details.vote_average
                    ? details.vote_average.toFixed(
                        1
                      )
                    : "N/A"}
                </span>

                <span>
                  ⏱️ {runtime}
                </span>

              </div>


              {details.genres &&
                details.genres.length > 0 && (

                  <div className="genres">

                    {details.genres.map(
                      (genre) => (

                        <span
                          key={genre.id}
                        >
                          {genre.name}
                        </span>

                      )
                    )}

                  </div>

                )}


              <p className="overview">
                {details.overview ||
                  "No description available for this film."}
              </p>


              <button
                className={`modal-watchlist ${
                  inWatchlist
                    ? "remove"
                    : ""
                }`}
                onClick={onToggle}
              >

                <Heart
                  size={18}
                  fill={
                    inWatchlist
                      ? "currentColor"
                      : "none"
                  }
                />

                {inWatchlist
                  ? "Remove from Watchlist"
                  : "Add to Watchlist"}

              </button>

            </>

          )}

        </div>

      </div>

    </div>
  );
}


export default App;