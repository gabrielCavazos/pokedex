import Modal from 'react-modal';
import './PokemonDetail.css';

function PokemonDetail({ pokemonDetail, modalIsOpen, setModalIsOpen }) {
  const customStyles = {
    content: {
      top: '50%',
      left: '50%',
      right: 'auto',
      bottom: 'auto',
      marginRight: '-50%',
      transform: 'translate(-50%, -50%)',
    },
  };

  function closeModal() {
    setModalIsOpen(false);
  }

  const {
    external_id,
    name,
    weight,
    height,
    active_abilities,
    not_active_abilities,
    types,
    image_url,
    favorite,
    hp,
    attack,
    defense,
    special_attack,
    special_defense,
    speed,
  } = pokemonDetail;

  return (
    <Modal
      isOpen={modalIsOpen}
      onRequestClose={closeModal}
      style={customStyles}
      contentLabel="Pokemon Details"
    >
      <div className="center">
        <img src={image_url} alt={name} className="pokemon-image" />
      </div>
      <h2>{name}</h2>
      <h3>Pokemon number: {external_id}</h3>
      <div className="pills-container">
        <div className="pill">Height: {height}</div>
        <div className="pill">Weight: {weight}</div>
      </div>

      <h3>Types:</h3>
      <div className="pills-container">
        {types &&
          types.map((type, index) => (
            <div key={index} className="pill">
              {type}
            </div>
          ))}
      </div>

      <h3>Active Abilities:</h3>
      <div className="pills-container">
        {active_abilities &&
          active_abilities.map((ability, index) => (
            <div key={index} className="pill">
              {ability}
            </div>
          ))}
      </div>

      <h3>Not Active Abilities:</h3>
      <div className="pills-container">
        {not_active_abilities &&
          not_active_abilities.map((ability, index) => (
            <div key={index} className="pill">
              {ability}
            </div>
          ))}
      </div>

      <h3>Base stats:</h3>
      <div className="pills-container">
        <div className="pill">HP: {hp}</div>
        <div className="pill">Attack: {attack}</div>
        <div className="pill">Defense: {defense}</div>
        <div className="pill">Special Attack: {special_attack}</div>
        <div className="pill">Special Defense: {special_defense}</div>
        <div className="pill">Speed: {speed}</div>
      </div>

      <button onClick={closeModal}>Close</button>
    </Modal>
  );
}

export default PokemonDetail;
