import Network.Data.OF13.Message
import Network.Data.OF13.Server

main :: IO ()
main = runServerOne 6633 factory
  where factory sw = handshake sw >> return (messageHandler sw)

handshake :: Switch -> IO ()
handshake sw = sendMessage sw [Hello { xid = 0, len = 8 }]

messageHandler :: Switch -> Maybe Message -> IO ()
messageHandler _ Nothing = putStrLn "Disconnecting"
messageHandler sw (Just msg) = print msg >> sendMessage sw [FeatureRequest 1]

