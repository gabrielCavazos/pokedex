import React, { useEffect, useState } from 'react';
import './App.css';
import ClipLoader from "react-spinners/ClipLoader";

import { ToastContainer } from 'react-toastify';

import Table from './Table';
import { notify, notifyError } from './helpers';
import PokemonDetail from './PokemonDetail';


function App() {
  const [data, setData] = useState([]);
  const [total, setTotal] = useState([]);
  const [avgWeight, setAvgWeight] = useState(0);
  const [avgHeight, setAvgHeight] = useState(0);
  const [pageNumber, setPageNumber] = useState(1);
  const [loading, setLoading] = useState(false);
  const [pokemonDetail, setPokemonDetail] = useState({});
  const [modalIsOpen, setModalIsOpen] = React.useState(false);


  useEffect(() => {
    const fetchData = () => {
      const url = `http://localhost:8000/api/pokemon/?page=${pageNumber}`;
      setLoading(true)
      fetch(url)
        .then(response => response.json())
        .then(responseData => {
          setData(responseData.results);
          setTotal(responseData.count);
          setAvgHeight(responseData.height_average);
          setAvgWeight(responseData.weight_average);
          setLoading(false)

        })
        .catch(error => {
          notifyError()
          setLoading(false)
        });
    };
    if(!loading){
      fetchData();
    }
  }, [pageNumber]);


  function openModal() {
    setModalIsOpen(true);
  }

 
  const handleFavorite = id => {
    const index = data.findIndex(pokemon => pokemon.id === id);

    const requestOptions = {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
    };
    const url = `http://localhost:8000/api/pokemon/${id}/`;
    fetch(url, requestOptions)
      .then(response => response.json())
      .then(data => {
        notify(data["weight_average"],data["height_average"],data["count"])
      })
      .catch(error => {
        notifyError()
      });

    setData(prevData => {
      const newData = [...prevData];
      newData[index].favorite = !newData[index].favorite;
      return newData;
    });
  };
  const handleDetail = id => {
    console.log("Detail of" + id)
    
    const fetchData = () => {
      const url = `http://localhost:8000/api/pokemon/${id}/`;
      fetch(url)
        .then(response => response.json())
        .then(responseData => {
          setPokemonDetail(responseData);
          openModal();
        })
        .catch(error => {
          console.log(error)
          notifyError()
        });
    };

    fetchData();
  };
  

  const handlePreviousPage = () => {
    setPageNumber(prevPageNumber => prevPageNumber - 1);
  };

  const handleNextPage = () => {
    setPageNumber(prevPageNumber => prevPageNumber + 1);
  };

  const override = {
    display: "block",
    margin: "0 auto",
    borderColor: "red",
  };
  const columns = [
    {
      Header: 'Favorite',
      accessor: 'favorite',
      Cell: ({ value }) => value,
    },
    {
      Header: 'Pokemon Number',
      accessor: 'external_id',
    },
    {
      Header: 'Name',
      accessor: 'name',
    },
    {
      Header: 'Height',
      accessor: 'height',
    },
    {
      Header: 'Weight',
      accessor: 'weight',
    },
    {
      Header: 'Abilities Count',
      accessor: 'abilities_count',
    },
    {
      Header: 'Active Abilities',
      accessor: 'active_abilities',
      Cell: ({ value }) => {
        const transformedAbilities = value.join(', ');
        return <span>{transformedAbilities}</span>;
      },
    },
    {
      id: "Detail", 
      Header: 'Detail',
      accessor: 'id',
      Cell: ({ value }) => {
        return <button onClick={() => handleDetail(value)}>View Details</button>
      },
    },
  ];


  return (
    <div className="App">
      <h1>Pokemons</h1>
      
      <div className="pills-container">
        <div className="pill">total: {total}</div>
        <div className="pill">Result per Page: {data.length}</div>
        <div className="pill">Avg Weight: {avgWeight}</div>
        <div className="pill">Avg Height: {avgHeight}</div>
      </div>
      <ToastContainer />
      <ClipLoader
        color="#ffffff"
        loading={loading}
        cssOverride={override}
        size={150}
        aria-label="Loading Spinner"
        data-testid="loader"
      />
      {loading && 
        <p>We are loading your pokemons! wait a min.</p>
      }
      {!loading && (
        <>
          <div className="pagination">
            <button
              className="pagination-button"
            onClick={handlePreviousPage}
              disabled={pageNumber === 1}
            >
              &lt;
            </button>
            <span className="pagination-page">{pageNumber}</span>
            <button className="pagination-button" onClick={handleNextPage}>
              &gt;
            </button>
          </div>
          <Table columns={columns} data={data} handleFavorite={handleFavorite} />
          <PokemonDetail pokemonDetail={pokemonDetail} modalIsOpen={modalIsOpen} setModalIsOpen={setModalIsOpen}></PokemonDetail>
        </>
      )}
 

    </div>
  );
}

export default App;
