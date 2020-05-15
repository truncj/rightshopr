import React from 'react'
import { Table } from 'react-bootstrap'

class SlotTableComponent extends React.Component {
  render() {
    if (this.props.slot){ 

      return (
        <Table striped bordered hover>
          <thead className="thead-dark" >
            <tr>
              <th>Store Name</th>
              <th>Available Slots</th>
            </tr>
          </thead>
          <tbody>
            {this.props.slot.map( slot =>
              <tr key={slot}>
                <td className="name-column">{slot[0]}</td>
                <td>{slot[1]}</td>
              </tr>
            )}
          </tbody>
        </Table>
      )
      
    }else{
      return null
    }
  }
}

export default SlotTableComponent