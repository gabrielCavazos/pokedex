import React, { useEffect, useState } from 'react';
import './App.css';
import { useTable } from 'react-table';
import { FaHeart, FaRegHeart } from 'react-icons/fa';
import ClipLoader from "react-spinners/ClipLoader";

import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function Table({ columns, data, handleFavorite }) {
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable({ columns, data });

  return (
    <table {...getTableProps()} className="table">
      <thead>
        {headerGroups.map(headerGroup => (
          <tr {...headerGroup.getHeaderGroupProps()}>
            {headerGroup.headers.map(column => (
              <th {...column.getHeaderProps()}>{column.render('Header')}</th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody {...getTableBodyProps()}>
        {rows.map(row => {
          prepareRow(row);
          return (
            <tr {...row.getRowProps()}>
              {row.cells.map(cell => (
                <td {...cell.getCellProps()}>
                  {cell.column.id === 'favorite' ? (
                    <FavoriteCell
                      value={cell.value}
                      handleFavorite={handleFavorite}
                      id={row.original.id}
                    />
                  ) : (
                    cell.render('Cell')
                  )}
                </td>
              ))}
            </tr>
          );
        })}
        <tr>
          <td colSpan={columns.length} className="empty-row"></td>
        </tr>
      </tbody>
    </table>
  );
}

function FavoriteCell({ value, handleFavorite, id }) {
  const handleToggleFavorite = () => {
    handleFavorite(id);
  };
  
  return (
    <span className="favorite-cell" onClick={handleToggleFavorite}>
      {value === true ? (
        <FaHeart className="heart-icon filled" />
      ) : (
        <FaRegHeart className="heart-icon" />
      )}
    </span>
  );
}


function App() {
  const [data, setData] = useState([]);
  const [total, setTotal] = useState([]);
  const [avgWeight, setAvgWeight] = useState(0);
  const [avgHeight, setAvgHeight] = useState(0);
  const [pageNumber, setPageNumber] = useState(1);
  const [loading, setLoading] = useState(false);

  const notify = (weight_average, height_average, count) => {
    toast(`Favorite data: avg weight:${weight_average} avg height:${height_average} count:${count}`)
  };
  
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


      });

    setData(prevData => {
      const newData = [...prevData];
      newData[index].favorite = !newData[index].favorite;
      return newData;
    });
  };

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
          console.error('Error fetching data:', error);
          setLoading(false)

        });
    };

    fetchData();
  }, [pageNumber]);

  const columns = [
    {
      Header: 'Favorite',
      accessor: 'favorite',
      Cell: ({ value }) => value,
    },
    {
      Header: 'Pokemon Number',
      accessor: 'id',
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
  ];
  
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
        </>
      )}
 

    </div>
  );
}

export default App;
