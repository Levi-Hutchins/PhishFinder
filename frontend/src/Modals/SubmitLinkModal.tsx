import React from "react"
import { LinkModalProps } from "../Components/Interfaces"

const LinkModal: React.FC<LinkModalProps> = ({isOpen, onClose}) =>{
    if(!isOpen){ return null}
    alert("Modals")
    return(
        <div className="modal-backdrop">
        <div className="modal-content">
          <button onClick={onClose}>Close</button>
          <p>TEst</p>
        </div>
      </div>
    );
}

export default LinkModal;