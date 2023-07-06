
import { useTable } from 'react-table';
import { FaHeart, FaRegHeart } from 'react-icons/fa';

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

export default Table;