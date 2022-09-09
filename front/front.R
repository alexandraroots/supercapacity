library(shinydashboard)
library(shiny)
library(shinythemes)
library(jsonlite)
library(httr)
library(plotly)


Axis_list <- c("Temperature_1", "Temperature_2", "Time_1", "Time_2", "Density")
url = 'https://9cf4-194-110-84-14.eu.ngrok.io/api/v1/smart_model/predict'
Structures <- c("nanoblades", "nanoflakes", "nanoflowers", "nanowires", "nanorods", "nanosheets", 
                "nanowall_network", "square-hexagonal_sheets", "urchin-like")

# Define UI
ui <- fluidPage(
  
  theme = shinytheme("cerulean"),
  titlePanel(h1("Supercapacitor", align = "center")),
  
    sidebarLayout(
      sidebarPanel(
                          
        #titlePanel("Choose Options"),
                          
        fluidRow(column(6,
                   sliderInput(inputId = "Temperature_1", label = "Hydrothermal Temperature", min = 80,
                               max = 200, value = c(120,160), width = "220px")),
                 column(6, ofset=3,         
                    sliderInput(inputId = "Time_1", label = "Hydrothermal Time", min = 1, max = 24,
                                value = 12, width = "220px"))
                ), 
        
        fluidRow(column(6,
                    sliderInput(inputId = "Velocity", label = "Velocity", min = 1, max = 10,
                                value = 2, width = "220px")),
                 column(6,
                    sliderInput(inputId = "Volume_solvent", label = "Volume of solvent", min = 10,
                              max = 500, value = 70, width = "220px")),
                ),
        
        fluidRow(column(6,
                   sliderInput(inputId = "Temperature_2", label = "Annealing Temperature", min = 200,
                                    max = 550, value = c(350,500), width = "220px")),
                 column(6, ofset=3,
                          
                   sliderInput(inputId = "Time_2", label = "Annealing Time", min = 1, max = 5,
                                    value = 2, width = "220px"))        
        ),
        
        fluidRow(column(6,
                   textInput(inputId = "Reagent_1", label = "Reagent 1", value = "Nickel(II) nitrate hexahydrate",
                             width = "220px")),
                 column(6, ofset = 3,  
                   textInput(inputId = "Reagent_2", label = "Reagent 2", value = "Cobalt(II) nitrate hexahydrate",
                             width = "220px"))
                ),  
        
        fluidRow(column(2,
                   radioButtons(inputId = "Measure_1", label = "Measure:",
                              choices = c("mmol", "g"), selected = "mmol")),
                 column(4, ofset=1,
                   textInput(inputId = "Mass_Reagent_1", label = "Mass Reagent 1",
                             value = "100", width = "100px")),
                 column(2, ofset=1,
                   radioButtons(inputId = "Measure_2", label = "Measure:",
                                choices = c("mmol", "g"), selected = "mmol")),
                 column(4, ofset=1, 
                   textInput(inputId = "Mass_Reagent_2", label = "Mass Reagent 2",
                             value = "100", width = "100px"))
                 
                 ),
                          
        fluidRow(column(6,
                   textInput(inputId = "Base", label = "Base", value = 'Urea',
                             width = "220px")),
                 column(2,
                   radioButtons(inputId = "Measure_3", label = "Measure:",
                                choices = c("mmol", "g"), selected = "mmol")),
                 column(3, ofset = 3,
                   textInput(inputId = "Mass_Base", label = "Mass Base",
                             value = "100", width = "100px"))
                 ),
                          
        fluidRow(column(6, 
                   sliderInput(inputId = "Density", label = "Density", min = 1, max = 70,
                                    value = 40, width = "220px")),
                 column(6,         
                   selectInput(inputId = "Axis_X", label = "Axis X", choices = Axis_list,
                               selected = "Temperature_1", width = "220px")),
                ),
        actionButton("Predict_Button", "Predict"),
        actionButton("Optimize_Button", "Optimize")),
      
        mainPanel(
               fluidRow(column(5, textOutput(outputId = "text1")),
                        column(5, ofset = 3, textOutput(outputId = "text2"))
               ),
               fluidRow(column(5, imageOutput("image1")),
                        column(5, ofset = 3, imageOutput("image2"))
                        ),
               
               textOutput(outputId = "value"),
               tags$head(tags$style("#value{color: black;
                                            font-size: 20px;
                                            font-style: gotic;
                                            }",
                                    "#text1{color: black;
                                            font-size: 20px;
                                            font-style: gotic;
                                            }",
                                    "#text2{color: black;
                                            font-size: 20px;
                                            font-style: gotic;
                                            }"
                                    
                                )),
               plotlyOutput("plot1"))
     
    )         
  )    
             

server <- function(input, output, session) {
 
md <- reactive({
    list(Temperature_1 = as.array(input$Temperature_1),
         Time_1 = as.numeric(input$Time_1),
         Velocity = as.numeric(input$Velocity),
         Temperature_2 = as.numeric(input$Temperature_2),
         Time_2 = as.numeric(input$Time_2),
         Base = as.character(input$Base),
         Measure_Base = as.character(input$Measure_1),
         Mass_Base = as.numeric(input$Mass_Base),
    
         Reagent_1 = as.character(input$Reagent_1),
         Measure_1 = as.character(input$Measure_2),
         Mass_Reagent_1 = as.numeric(input$Mass_Reagent_1),
    
         Reagent_2 = as.character(input$Reagent_2),
         Measure_2 = as.character(input$Measure_3),
         Mass_Reagent_2 = as.numeric(input$Mass_Reagent_2),
    
         Volume_solvent = as.numeric(input$Volume_solvent),
         Density = as.numeric(input$Density),
         Axis_x = as.character(input$Axis_X))

         })
  
get_predict <- function(md, target){
  md$ target <- target
  rand = sample(x = 1:9, size = 1, replace = TRUE)
  name = paste(Structures[rand], '.jpg', sep="")
  name_png = paste(Structures[rand], '.png', sep="")
  predict <- POST(url, body = md, encode = "json", verbose())
  predict <- jsonlite::fromJSON(content(predict, "text"), flatten = TRUE)
  
  output$value <- renderText({paste("Capacity: ",round(predict$ capacity))})
  output$text1 <- renderText({"Microstructure shpinel"})
  output$text2 <- renderText({"Crystal structure shpinel"})

  output$image1 <- renderImage({
    if (is.null(predict$ label))
      return(NULL)
    else {
      #name = predict$ structure
      return(list(
        src = paste('micro/', name, sep=""),
        filetype = "image/jpeg",
        alt = "This is a Chrysanthemum",
        width = 300,
        height = 300))
    }
  }, deleteFile = FALSE)
  
  output$image2 <- renderImage({
    if (is.null(predict$ label))
      return(NULL)
    else {
      
      return(list(
        src = paste('structure/', name_png, sep=""),
        filetype = "image/png",
        alt = "This is a Chrysanthemum",
        width = 300,
        height = 300))
    }
  }, deleteFile = FALSE)
  
 # df <- list(predict$ ax_x, predict$ ax_y)
  #names(df) <- c(input$Axis_X, 'Capacity')
  #df <- as.data.frame(df)
  #print(df[1])
  output$plot1 <- renderPlotly({
    plot_ly(x=predict$ ax_x, y=predict$ ax_y, type = 'scatter', mode = 'lines')%>%
    layout(title = '', xaxis = list(title = input$Axis_X), yaxis = list(title = 'Capacity'))%>% 
    layout(height = 275, width = 600)
    
  })
  
  return(predict)}
  

observeEvent(input$Predict_Button, {
  md <- md()
  predict <- get_predict(md, 'predict')
  })
  
observeEvent(input$Optimize_Button, {
  md <- md()
  predict <- get_predict(md, 'optimize')
  predict <- predict$ parameters
  
  updateSliderInput(session, 'Temperature_1', value = c(as.numeric(predict$ Temperature_1), as.numeric(predict$ Temperature_1)))
  updateSliderInput(session, 'Time_1', value = as.numeric(predict$ Time_1))
  updateSliderInput(session, 'Velocity', value = predict$ Velocity)
  updateSliderInput(session, 'Temperature_2', value = c(as.numeric(predict$ Temperature_2), as.numeric(predict$ Temperature_2)))
  updateSliderInput(session, 'Time_2', value = predict$ Time_2)
  #updateTextInput(session, 'Base', value = predict$ Base)
  #updateTextInput(session, 'Mass_Base', value = predict$ Mass_Base)
  updateTextInput(session, 'Reagent_1', value = predict$ Reagent_1)
  updateTextInput(session, 'Mass_Reagent_1', value = predict$ Mass_Reagent_1)
  updateTextInput(session, 'Reagent_2', value = predict$ Reagent_2)
  updateTextInput(session, 'Mass_Reagent_2', value = predict$ Mass_Reagent_2)
  updateSliderInput(session, 'Volume_solvent', value = predict$ Volume_solvent)
  updateSliderInput(session, 'Density', value = predict$ Density)
  updateRadioButtons(session, 'Measure_1', selected = "mmol")
  updateRadioButtons(session, 'Measure_2', selected = "mmol")
  updateRadioButtons(session, 'Measure_3', selected = "mmol")
  })
}

shinyApp(ui, server)