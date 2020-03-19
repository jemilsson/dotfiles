{-# LANGUAGE OverloadedStrings #-}
import System.Taffybar
import System.Taffybar.Information.CPU
import System.Taffybar.SimpleConfig
import System.Taffybar.Widget
import System.Taffybar.Widget.Generic.Graph
import System.Taffybar.Widget.Generic.PollingGraph
import System.Taffybar.Widget.SimpleClock
import System.Taffybar.Widget.Battery
import System.Taffybar.Widget.CommandRunner
import System.Taffybar.Widget.Generic.PollingLabel

cpuCallback = do
  (_, systemLoad, totalLoad) <- cpuLoad
  return [ totalLoad, systemLoad ]

main = do
  let cpuCfg = defaultGraphConfig { graphDataColors = [ (0, 1, 0, 1), (1, 0, 1, 0.5)]
                                  , graphLabel = Just "\62171 cpu"
                                  }
      clock = textClockNewWith defaultClockConfig {
        clockUpdateStrategy = RoundedTargetInterval 1 0.0,
        clockFormatString = "\61463 %a, %Y-%m-%d %H:%M:%S"
      }
      cpu = pollingGraphNew cpuCfg 0.5 cpuCallback

      workspaces = workspacesNew defaultWorkspacesConfig {
        getWindowIconPixbuf = scaledWindowIconPixbufGetter getWindowIconPixbufFromEWMH
      }
      simpleConfig = defaultSimpleTaffyConfig {
                        barHeight = 12,
                        barPadding = 0,
                        startWidgets = [ workspaces ],
                        endWidgets = [
                          sniTrayNew,
                          clock,
                          cpu,
                          textBatteryNew "$percentage$ $time$",
                          batteryIconNew
                          ]
                       }
  simpleTaffybar simpleConfig
