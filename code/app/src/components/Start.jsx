import { useNavigate } from "react-router-dom";
import { Button  } from "@mui/material";
import {createTheme,ThemeProvider} from '@mui/material/styles';
import { Link } from "react-router-dom";
import ChessBoardImg from "../assets/background2.jpg";
import ImageScacchi from "../assets/logo.png";
import ImageSinglePlayer from "../assets/singleplayer-removebg-preview.png";
import ImageMultiPlayer from "../assets/multiplayer-removebg-preview.png";
import { Image, Nav, Modal, Form, FloatingLabel, CloseButton} from "react-bootstrap";
import { useState, useEffect } from "react";
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import io from 'socket.io-client';

function Start(props){

    const theme = createTheme({
        palette: {
          brown: {
            main: '#795548',
            light: '#543b32',
            dark: '#543b32',
            contrastText: '#fff',
          },
        },
      });

    const navigator = useNavigate();
    
    const [showOptions, setShowOptions] = useState(false);

    const [showModal, setShowModal] = useState(false);


    function handleSubmit (e) {
        e.preventDefault();
        if(props.botDiff === 0)
            props.setBotDiff(1);
        setShowModal(false);
        props.socket.emit('start', {
            type: props.setIsSinglePlayer,
            rank: props.setGameImb, // qual' e' il rank?
            time: props.setGameTime
        });
        navigator(`./game`, { relative: "path" });
    }


    useEffect(()=>{
        props.setSocket(io("ws://localhost:8766"));
    },[])

    return (
        <>

        <Modal  show={showModal} centered size="lg">
            <Modal.Title  style={{display: "flex", justifyContent: "flex-end", backgroundColor: "#b6884e"}}>
                <CloseButton style={{marginRight: "10px", marginTop: "5px"}} onClick={()=> setShowModal(false)}/>
            </Modal.Title>
            <Modal.Body style={{backgroundColor: "#b6884e"}}>
                <Form onSubmit={handleSubmit} >
                    {props.isSinglePlayer &&
                        <FloatingLabel
                            controlId="floatingInput1"
                            label="Bot Difficult"
                            className="mb-3"
                        >
                            <Form.Control value={props.botDiff} onChange={(e)=>{if(e.target.value > 20 || e.target.value < 0) props.setBotDiff(1); else props.setBotDiff(e.target.value); }} required type="number" min={1} max={20}  placeholder="value from 1 to 20" />
                        </FloatingLabel>
                    }
                    <FloatingLabel
                        controlId="floatingInput2"
                        label="Game Imbalance"
                        className="mb-3"
                    >
                        <Form.Control required value={props.gameImb} onChange={(e)=>{if(e.target.value > 100 || e.target.value < 0) props.setGameImb(0); else props.setGameImb(e.target.value); }}  type="number" min={0} max={100}  placeholder="value from 0 to 100" />
                    </FloatingLabel>
                    {!props.isSinglePlayer &&
                        <FloatingLabel
                            controlId="floatingInput3"
                            label="Game Time in sec"
                            className="mb-3"
                        >
                            <Form.Control required value={props.gameTime} onChange={(e)=>{if(e.target.value < 0) props.setGameTime(3000); else props.setGameTime(e.target.value);}}  type="number" min={1}   placeholder="value from 1 " />
                        </FloatingLabel>
                    }
                        <div style={{display: "flex", justifyContent: "flex-end"}}>
                            <Button size="large" color="primary" type="submit" variant="contained">avvia</Button>
                        </div>
                </Form>
            </Modal.Body>
        </Modal>


            
            <div style={{fontFamily: "Helvetica Neue", backgroundImage: `${!showOptions ?  `url(${ChessBoardImg})` : "" }`, backgroundSize: "cover", backgroundAttachment: "fixed", backgroundRepeat: "no-repeat", backgroundColor: `${showOptions ? "#b99b69" : ""}`, width: "100vw", height: "100vh"}}> 
                <ThemeProvider theme={theme}>

                <div style={{ paddingTop: "20vh"}}>
                    {!showOptions ? 
                    <>
                        <div style={{display: "flex", justifyContent: "center"}}>
                            <div>
                                <Image src={`${ImageScacchi}`} style={{width: "100px", height: "100px", opacity: 0.8, marginTop: "-60px"}} alt="immagine di scacchi" />
                                <span style={{color: "white", fontSize: "5rem"}}>ChessVerse</span>
                            </div>
                        </div>
                        
                        <div style={{display: "flex", justifyContent: "center"}}>
                            <div>
                                <p style={{color: "white", fontSize: "3rem"}}>Challenge yourself, Challenge the world</p>
                            </div>
                        </div>
                        
                        <div style={{display: "flex", justifyContent: "center", marginTop: "40px"}}>
                            <div>
                                <Nav.Link as={Link} to="/login">
                                    <Button color="brown" disabled={true}  style={{fontSize: "1.5rem"}}  variant="contained" >
                                    Log In
                                    </Button>
                                </Nav.Link>
                            </div>
                        </div>
                        <div style={{display: "flex", justifyContent: "center", marginTop: "30px"}}>
                            <div>
                                <Button color="brown"  style={{fontSize: "1.5rem"}} onClick={()=>{setShowOptions(true)}}  variant="contained" >
                                    Play as guest
                                </Button>
                            </div>
                        </div>
                    </>
                    : 
                    <>
                        <div style={{display: "flex", justifyContent: "center"}}>
                            <div>
                                <p style={{color: "white", fontSize: "5rem"}}>Choose an option:</p>
                            </div>
                        </div>
                        <div style={{display: "flex", justifyContent: "center", marginTop: "30px"}}>
                            <div>
                                    <Button color="brown"  onClick={()=>{props.setIsSinglePlayer(true); setShowModal(true)}} style={{fontSize: "1.5rem", borderRadius: "20px"}}  variant="contained" >
                                        <div style={{marginTop: "5px", marginBottom: "5px", marginRight: "30px", marginLeft: "30px"}}>
                                            <Image src={`${ImageSinglePlayer}`} style={{width: "30px", height: "30px", marginBottom: "-5px", marginRight: "5px"}} alt="immagine di scacchi SinglePlayer" />
                                            <span>Single Player</span>
                                        </div> 
                                    </Button>     
                            </div>
                        </div>
                        <div style={{display: "flex", justifyContent: "center", marginTop: "30px"}}>
                            <div>
                                    <Button color="brown" onClick={()=>{props.setIsSinglePlayer(false); setShowModal(true);}} style={{fontSize: "1.5rem", borderRadius: "20px"}}  variant="contained" >
                                        <div style={{marginTop: "5px", marginBottom: "5px"}}>
                                            <Image src={`${ImageMultiPlayer}`} style={{width: "50px", height: "30px", marginBottom: "-5px", marginRight: "10px"}} alt="immagine di scacchi SinglePlayer" />
                                            <span>MultiPlayer</span>
                                        </div>  
                                    </Button>
                            </div>
                        </div>
                        <div style={{display: "flex", justifyContent: "center", marginTop: "30px"}}>
                            <div>
                                <Button color="brown" style={{fontSize: "1.5rem", borderRadius: "20px"}} onClick={()=>setShowOptions(false)} variant="contained" >
                                    <div style={{marginTop: "5px", marginBottom: "5px"}}>
                                        <HighlightOffIcon style={{marginRight: "10px", marginTop: "-3px"}} fontSize="large"/>
                                        <span>Quit</span>
                                    </div>
                                    
                                </Button>
                            </div>
                        </div>
                    </>
                    }
                </div>
                </ThemeProvider>

            </div>
                
        </>
    )
}

export default Start;


