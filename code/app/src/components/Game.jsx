import ImageScacchi from "../assets/logo.png";
import { useEffect, useLayoutEffect, useRef, useState } from "react";
import { Card, Col, Image, Modal, Nav, Row } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { Gear, ExclamationDiamond } from 'react-bootstrap-icons';
import { Button  } from "@mui/material";
import "../styles/Game.css";
import useWindowDimensions from "./useWindowDimensions.jsx";
import { PVP } from "../const/const.js";
import ImageBlackTime from "../assets/blackTime.png";
import ImageWhiteTime from "../assets/whiteTime.png";
import Board from "./Board.jsx";
import PropTypes from "prop-types";

function Game({
  gameTime,
  isLoadingGame, setIsLoadingGame,
  socket, setSocket,
  data,
  mode,
  startFen,
  color,
  roomId
}) {
    const { width, height } = useWindowDimensions();
    const [fontSize, setFontSize] = useState("20px");

    useLayoutEffect(()=>{
        if(width < 440)
            setFontSize("18px");
        else if((width > 440) && (width < 540))
            setFontSize("22px");
        else
            setFontSize("26px");
    },[width]);

    const defaultTime = new Date();
    defaultTime.setSeconds(defaultTime.getSeconds() + gameTime);

    const navigator = useNavigate();
    const [moves, setMoves] = useState([]);
    const [showModalMenu, setShowModalMenu] = useState(false);
    const [showGameOver, setShowGameOver] = useState(false);
    const [showVictory, setShowVictory] = useState(false);
    const [showTie, setShowTie] = useState(false);
    const [timers, setTimers] = useState([gameTime, gameTime]);
    const [timerInterval, setTimerInterval] = useState(null);
    const [turn, setTurn] = useState(null);
    const [game, setGame] = useState(null);
    const movesRef = useRef(null);

    useEffect(() => {
        if (turn === null) return;
        const interval = 100;
        if (timerInterval !== null)
            clearInterval(timerInterval);
        setTimerInterval(setInterval(() => {
            setTimers((prevTime) => {
                const updatedTime = [...prevTime];
                updatedTime[Number(game.turn()==="b")]-=interval/1000;
                return updatedTime;
                });
        }, interval));
    
        return () => {
            clearInterval(timerInterval);
            setTimerInterval(null);
        }
      }, [turn]);


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

    function handleMenu(){
        socket.emit("resign", {type: mode, id: roomId});
        setSocket(undefined);
    }

    function handleUndo (){
        socket.emit("pop", {type: mode, id: roomId});
    }

    useEffect(()=>{
        movesRef.current.scrollTo({
            top: movesRef.current.scrollHeight,
            behavior: "smooth",
        });
        
    },[moves]);

    //questo useEffect serve a fare in modo che se refreshi game ti fa tornare al menu
    useEffect(()=>{
        if (socket === undefined || socket === null) {
            navigator(`../`, { relative: "path" });
        }
    }, [socket]);

    return (
        <div data-testid="game">
            <Modal
              show={showGameOver}
              centered
              dialogClassName="my-modal"
            >
                <div style={{border: "4px solid red"}}>
                    <Modal.Body style={{backgroundColor: "#b6884e"}}>
                        <div style={{display: "flex", justifyContent: "center", fontSize: `${fontSize}`}}>
                            <span style={{fontWeight: "bold", marginRight: "10px"}}>Game Over</span>
                            <ExclamationDiamond size={40} color="red" />
                        </div>
                        <div style={{display: "flex", justifyContent: "space-around", marginTop: "20px", marginBottom: "15px"}}>
                            <ThemeProvider theme={theme}>
                                <Nav.Link
                                  as={Link}
                                  to="/"
                                  style={{display: "flex", justifyContent: "center"}}
                                >
                                    <Button
                                      style={{fontSize: "1.2rem"}}
                                      size="large"
                                      color="brown"
                                      onClick={() => {socket.emit("resign", {type: mode, id: roomId}); 
                                                        setSocket(undefined);
                                                    }}
                                      variant="contained"
                                    >
                                        Return to menu
                                    </Button>
                                </Nav.Link>
                            </ThemeProvider>
                        </div>
                    </Modal.Body>
                </div>
            </Modal>

            <Modal
              show={showVictory}
              centered
              dialogClassName="my-modal"
            >
                <div style={{border: "4px solid green"}}>
                    <Modal.Body style={{backgroundColor: "#b6884e"}}>
                        <div style={{display: "flex", justifyContent: "center", fontSize: `${fontSize}`}}>
                            <span style={{fontWeight: "bold", marginRight: "10px"}}>You won!</span>
                            <ExclamationDiamond size={40} color="green" />
                        </div>
                        
                        <div style={{display: "flex", justifyContent: "space-around", marginTop: "20px", marginBottom: "15px"}}>
                            <ThemeProvider theme={theme}>
                                <Nav.Link
                                  as={Link}
                                  to="/"
                                  style={{display: "flex", justifyContent: "center"}}
                                >
                                    <Button
                                      style={{fontSize: "1.2rem"}}
                                      size="large"
                                      color="brown"
                                      onClick={() => {setSocket(undefined); }}
                                      variant="contained"
                                    >
                                        Return to menu
                                    </Button>
                                </Nav.Link>
                            </ThemeProvider>
                        </div>
                    </Modal.Body>
                </div>
            </Modal>


            <Modal
              show={showTie}
              centered
              dialogClassName="my-modal"
            >
                <div style={{border: "4px solid gray"}}>
                    <Modal.Body style={{backgroundColor: "#b6884e"}}>
                        <div style={{display: "flex", justifyContent: "center", fontSize: `${fontSize}`}}>
                            <span style={{fontWeight: "bold", marginRight: "10px"}}>It's a tie!</span>
                            <ExclamationDiamond size={40} color="gray" />
                        </div>
                        
                        <div style={{display: "flex", justifyContent: "space-around", marginTop: "20px", marginBottom: "15px"}}>
                            <ThemeProvider theme={theme}>
                                <Nav.Link
                                  as={Link}
                                  to="/"
                                  style={{display: "flex", justifyContent: "center"}}
                                >
                                    <Button
                                      style={{fontSize: "1.2rem"}}
                                      size="large"
                                      color="brown"
                                      onClick={() => {setSocket(undefined); }}
                                      variant="contained"
                                    >
                                        Return to menu
                                    </Button>
                                </Nav.Link>
                            </ThemeProvider>
                        </div>
                    </Modal.Body>
                </div>
            </Modal>

            <Modal
              show={showModalMenu}
              centered
              dialogClassName="my-modal"
            >
                <Modal.Body style={{backgroundColor: "#b6884e", fontSize: `${fontSize}`}}>
                    <div style={{display: "flex", justifyContent: "center"}}>
                        <p>Are you sure you want to go back</p>
                    </div>
                    <div style={{display: "flex", justifyContent: "center"}}>
                        <p>to the main menu?</p>
                    </div>
                    <div style={{display: "flex", justifyContent: "space-around", marginTop: "20px", marginBottom: "15px"}}>
                        <ThemeProvider theme={theme}>
                            <Button
                              style={{fontSize: "1.2rem"}}
                              size="large"
                              color="brown"
                              onClick={()=> setShowModalMenu(false)}
                              variant="contained"
                            >
                                No
                            </Button>
                            <Nav.Link as={Link} to="/">
                                <Button
                                  style={{fontSize: "1.2rem"}}
                                  size="large"
                                  color="brown"
                                  onClick={(e)=> {
                                      e.stopPropagation();
                                      handleMenu();
                                  }}
                                  variant="contained"
                                >
                                    Yes
                                </Button>
                            </Nav.Link>
                        </ThemeProvider>
                    </div>
                </Modal.Body>
            </Modal>

            <div style={{backgroundColor: "#b99b69", width: "100vw", height: "100vh", overflow: "auto", overflowX: "hidden"}}>
                <ThemeProvider theme={theme}>
                <div style={{paddingTop: "10px", paddingLeft: "10px"}}>
                    <Row>
                        <Col>
                            <Row style={{marginBottom: "20px"}}>
                                <Col style={{display:"flex", justifyContent:"flex-end"}}>
                                    <div style={{marginTop: "20px", display: "flex", justifyContent: "center"}}>
                                        <img src={`${ImageWhiteTime}`} alt="clock white" style={{maxWidth: "30px", maxHeight: "30px", marginTop: "-6px"}}/>
                                        <div style={{textAlign: 'center'}}>
                                            <span>{`${String(Math.floor(timers[0] / 60)).padStart(2, '0')}:${String(Math.floor(timers[0] % 60)).padStart(2, '0')}`}</span>
                                        </div>
                                        {mode === PVP &&
                                            <>
                                                <span style={{marginLeft: "20px"}}></span>
                                                <img src={`${ImageBlackTime}`} alt="clock black" style={{maxWidth: "30px", maxHeight: "30px", marginTop: "-6px"}}/>
                                                <div style={{textAlign: 'center'}}>
                                                    <span>{`${String(Math.floor(timers[1] / 60)).padStart(2, '0')}:${String(Math.floor(timers[1] % 60)).padStart(2, '0')}`}</span>
                                                </div>
                                            </>
                                        }
                                        </div>
                                </Col>
                                <Col style={{display:"flex", justifyContent:"flex-end", marginRight: "-200px"}}>
                                    <Image src={`${ImageScacchi}`} style={{width: "50px", height: "50px", opacity: 0.8}} alt="immagine di scacchi" />
                                        <span style={{color: "white", fontSize: "2.7rem"}}>ChessVerse</span>
                                </Col>
                            </Row>
                        </Col>
                        <Col style={{display: "flex", justifyContent: "flex-end", marginRight: "40px"}}>
                            <Button
                              color="brown"
                              onClick={()=> setShowModalMenu(true)}
                              style={{fontSize: "1.5rem"}}
                              variant="contained"
                            >
                                <Gear size={30} />
                            </Button>
                        </Col>
                    </Row>
                </div>
                <Row>
                    <Col>
                        <div style={{display: "flex", justifyContent: "center"}}>
                            <div>
                                <Board
                                  navigator={navigator}
                                  setShowVictory={setShowVictory}
                                  setShowTie={setShowTie}
                                  width={width}
                                  height={height}
                                  setShowGameOver={setShowGameOver}
                                  setMoves={setMoves}
                                  data={data}
                                  isLoadingGame={isLoadingGame}
                                  setIsLoadingGame={setIsLoadingGame}
                                  socket={socket}
                                  setSocket={setSocket}
                                  mode={mode}
                                  startFen={startFen}
                                  color={color}
                                  setTurn={setTurn}
                                  updateTimers={setTimers}
                                  roomId={roomId}
                                  game={game}
                                  setGame={setGame}
                                />
                            </div>
                        </div>
                    </Col>
                    <Col style={{maxWidth:"50vw"}}>
                    <Row>
                    <Col>
                    <Card style={{marginLeft: "30px", backgroundColor: "#b6884e", marginTop: "120px", marginRight: "10px"}}> 
                            <Card.Title style={{display: 'flex', justifyContent: "center"}}>
                                <p style={{fontWeight: "bold", fontSize: `${fontSize}`, marginTop: "5px"}}>
                                    Moves History
                                </p>
                            </Card.Title>
                            <Card.Body ref={movesRef} style={{overflow: "auto", height: `calc(${height}px / 2)`, marginLeft: "20px", marginBottom: "20px", overflowY:"auto"}}>
                                <Row>
                                    <Col sm={2}>
                                        {moves.map((el, i) =>{
                                            if(i % 2 === 0) {
                                                return (
                                                    <span  style={{fontWeight: "bold", display: "flex", alignItems: "center", paddingTop: "8px", paddingBottom: "8px", marginBottom: "10px", }} key={i}> 
                                                        {Math.floor(i/2)+1}.
                                                    </span>
                                                )
                                            }
                                        })
                                        
                                        }
                                    </Col>
                                    <Col sm={5}>
                                    {moves.map((el,i) => {
                                        if(i % 2 === 0) {
                                            return (
                                                    <Card style={{marginBottom: "10px", backgroundColor: "#9f7a48", border: `3px solid white`, display: "flex", alignItems: "center" }} key={i}>         
                                                        <span style={{paddingTop: "5px", paddingBottom: "5px"}}>{el}</span>
                                                    </Card>
                                                
                                            )
                                        }
                                    })}
                                    </Col>
                                    <Col sm={5}>
                                    {moves.map((el,i) => {
                                        if(i % 2 === 1){
                                            return (
                                              <Card style={{
                                                  marginBottom: "10px",
                                                  backgroundColor: "#9f7a48",
                                                  border: `3px solid black`,
                                                  display: "flex",
                                                  alignItems: "center"
                                              }} key={i}
                                              >
                                                  <span style={{paddingTop: "5px", paddingBottom: "5px"}}>
                                                      {el}
                                                  </span>
                                              </Card>
                                            )
                                        }
                                    })}
                                    </Col>
                                </Row>
                                <Row>
                                    <div style={{paddingTop: "20px"}}>
                                        <Button disabled={moves.length === 0} color="brown" style={{width: "100%", fontSize: `${fontSize}`}} onClick={handleUndo}  variant="contained" >Undo</Button>
                                    </div>
                                </Row>
                            </Card.Body>
                        </Card>
                    </Col>
                    </Row>
                    </Col>
                </Row>
                </ThemeProvider>
            </div>
        </div>
    );
}

Game.propTypes = {
    gameTime: PropTypes.number,
    isLoadingGame: PropTypes.bool,
    setIsLoadingGame: PropTypes.func,
    socket: PropTypes.object,
    setSocket: PropTypes.func,
    mode: PropTypes.number,
    data: PropTypes.object,
    startFen: PropTypes.string,
    color: PropTypes.string,
    roomId: PropTypes.string
}

export default Game;