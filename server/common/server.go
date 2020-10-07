package common

import (
	"bufio"
	//"fmt"
	"net"
	//"time"

	log "github.com/sirupsen/logrus"
)

// ServerConfig Configuration used by the server
type ServerConfig struct {
	Port			string
	ListenBacklog 	string
}

// Server Entity that encapsulates how
type Server struct {
	config 	ServerConfig
	conns   chan net.Conn
}

// NewServer Initializes a new server receiving the configuration as a parameter
func NewServer(config ServerConfig) *Server {
	server := &Server {
		config: config,
	}
	return server
}

// Accepting connections
func (s *Server) acceptConnections(listener net.Listener) chan net.Conn {
	channel := make(chan net.Conn)

	go func() {
		for {
			client, err := listener.Accept()

			if client == nil || err != nil {
				log.Errorf("[SERVER] Couldn't accept client", err)
				continue
			}

			log.Infof("[SERVER] Client accepted at %s", client.RemoteAddr().String())
			channel <- client
		}
	}()

	return channel
}

func (s *Server) handleConnections(client net.Conn) {
	buffer := bufio.NewReader(client)

	for {
		line, err := buffer.ReadBytes('\n')

		if err != nil {
			break
		}

		client.Write(line)
	}
}

// Run start listening for client messages
func (s *Server) Run() {
	// Create server
	listener, _ := net.Listen("tcp", ":" + s.config.Port)
	if listener == nil {
		log.Fatalf("[SERVER] Error creating TCP server socket at port %s.", s.config.Port)
	}

	// Start processing connections
	s.conns = s.acceptConnections(listener)

	// Start parallel messages echo
	for {
		go s.handleConnections(<-s.conns)
	}
}
