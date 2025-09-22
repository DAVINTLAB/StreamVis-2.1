"""
Página de Classificação de Texto
Implementa o fluxo completo de classificação de texto em 5 etapas
"""
import streamlit as st
import pandas as pd
import os
import pathlib
from datetime import datetime
import io

# =============================================================================
# Data Treatment to Open Screen
# =============================================================================

def generate_download_data(dataframe, format_type, filename):
    """
    Gera os dados em diferentes formatos para download
    """
    if format_type == 'csv':
        buffer = io.StringIO()
        dataframe.to_csv(buffer, index=False)
        return buffer.getvalue().encode('utf-8'), f"{filename}.csv", "text/csv"

    elif format_type == 'xlsx':
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            dataframe.to_excel(writer, index=False, sheet_name='Classificacao')
        return buffer.getvalue(), f"{filename}.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    elif format_type == 'json':
        buffer = io.StringIO()
        dataframe.to_json(buffer, orient='records', indent=2)
        return buffer.getvalue().encode('utf-8'), f"{filename}.json", "application/json"

    elif format_type == 'parquet':
        buffer = io.BytesIO()
        dataframe.to_parquet(buffer, index=False)
        return buffer.getvalue(), f"{filename}.parquet", "application/octet-stream"

    else:
        raise ValueError(f"Formato não suportado: {format_type}")

# =============================================================================
# Data Treatment to Open Screen
# =============================================================================

# Check if there is a current task being edited
if 'currentTaskInEdition' not in st.session_state or st.session_state.currentTaskInEdition is None:
    st.warning("⚠️ Nenhuma tarefa em edição. Por favor, crie uma nova tarefa na página inicial.")
    st.switch_page("Home.py")
    st.stop()

# Check if the current task is of the correct type
if st.session_state.currentTaskInEdition.taskType != "Classificação de Texto":
    st.error("⚠️ Tipo de tarefa incorreto. Esta página é para classificação de texto.")
    st.session_state.currentTaskInEdition = None
    st.switch_page("Home.py")
    st.stop()

# Initialize dataset state
if 'datasetLoaded' not in st.session_state:
    st.session_state.datasetLoaded = False

# =============================================================================
# Header from Screen
# =============================================================================

# Page configuration
st.set_page_config(page_title="Classificação de Texto - ML Hub", page_icon="📝", layout="wide", initial_sidebar_state="collapsed")

# CSS to hide default sidebar
st.markdown('<style> .css-1d391kg { display: none; } .css-164nlkn { display: none; } [data-testid="stSidebar"] { display: none; } .css-1lcbmhc { display: none; } </style>', unsafe_allow_html=True)

# Create header with return button
header_col1, header_col2 = st.columns([8, 2])

with header_col1:
    # Page tittle
    st.markdown("# 📝 Classificação de Texto")
    st.markdown("Execute classificação de texto usando modelos de Machine Learning de forma simples e intuitiva.")

with header_col2:
    # Return to home button
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    if st.button("🏠 Voltar ao Início", use_container_width=True):
        st.switch_page("Home.py")

st.markdown("---")

# =============================================================================
# Step 1: Task Setup
# =============================================================================

st.markdown("### Etapa 1: Configuração da Tarefa")

# Task name
taskName = st.text_input(
    "Defina o nome da sua tarefa de classificação de texto.",
    value=st.session_state.currentTaskInEdition.taskName,
    placeholder="Ex: Análise de Sentimento - Reviews de Produtos",
    help="Escolha um nome descritivo para identificar sua tarefa"
)

# Update current task
st.session_state.currentTaskInEdition.SetTaskName(taskName)
st.session_state.currentTaskInEdition.SetTaskType("Classificação de Texto")

# Check if the fields are filled in
if taskName.strip():
    taskConfigured = True
    st.success("✅ Configuração da tarefa concluída!")
else:
    taskConfigured = False
    st.warning("⚠️ Preencha o nome da tarefa para continuar.")

st.markdown("---")

# =============================================================================
# Step 2: Dataset Selection
# =============================================================================

st.markdown("### Etapa 2: Seleção do Dataset")
st.markdown("Faça upload de um novo arquivo para classificação de texto.")

uploadedFile = st.file_uploader("", type=['csv', 'json', 'xlsx', 'xls'])

if uploadedFile is not None:
    try:
        # Save file temporarily
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploadedFile.name.split('.')[-1]}") as temporarilyFile:
            temporarilyFile.write(uploadedFile.getvalue())
            temporarilyPath = temporarilyFile.name

        selectedDataset = {
            'name': uploadedFile.name,
            'path': temporarilyPath,
            'size': len(uploadedFile.getvalue())
        }

        # Load and visualize automatically
        try:
            # Configure dataset in current task
            st.session_state.currentTaskInEdition.SetInputDatasetPath(selectedDataset['path'])
            st.session_state.currentTaskInEdition.LoadInputDataset()
            st.session_state.datasetLoaded = True

        except Exception as e:
            st.error(f"❌ Erro ao carregar dataset: {str(e)}")

    except Exception as e:
        st.error(f"Erro ao carregar arquivo: {str(e)}")

# Preview the dataset if loaded
if st.session_state.datasetLoaded and st.session_state.currentTaskInEdition is not None:
    st.markdown("#### Preview do Dataset")

    dataset = st.session_state.currentTaskInEdition.inputDataset

    if dataset is not None:
        # General information
        column1, column2, column3 = st.columns(3)

        with column1:
            st.metric("Linhas", len(dataset))
        with column2:
            st.metric("Colunas", len(dataset.columns))
        with column3:
            st.metric("Memória", f"{dataset.memory_usage(deep=True).sum() / 1048576:.2f} MB")

        # Preview the data
        st.markdown("**Primeiras 10 linhas:**")
        st.dataframe(dataset.head(10), use_container_width=True)

        # Columns information
        st.markdown("**Informações das Colunas:**")
        column_info = pd.DataFrame({
            'Coluna': dataset.columns,
            'Tipo': dataset.dtypes.astype(str),
            'Valores Únicos': [dataset[col].nunique() for col in dataset.columns],
            'Valores Nulos': [dataset[col].isnull().sum() for col in dataset.columns],
            'Exemplo': [str(dataset[col].iloc[0])[:50] + "..." if len(str(dataset[col].iloc[0])) > 50
                        else str(dataset[col].iloc[0]) for col in dataset.columns]
        })
        st.dataframe(column_info, use_container_width=True)

        # Suggested text columns
        textColumns = [col for col in dataset.columns if dataset[col].dtype == 'object']

        selectedTextColumn = st.selectbox(
            "Selecione a coluna que contém o texto para classificação:",
            options=textColumns,
            help="Esta coluna será usada como entrada para o modelo de classificação"
        )

        # Store selected column in session state
        if 'selectedTextColumn' not in st.session_state:
            st.session_state.selectedTextColumn = None

        if selectedTextColumn:
            st.session_state.selectedTextColumn = selectedTextColumn

        # Preview of selected column
        if selectedTextColumn:
            st.markdown("#### Preview da Coluna Selecionada")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total de Linhas", len(dataset))
            with col2:
                nonEmptyTexts = dataset[selectedTextColumn].dropna().astype(str).str.strip().ne('').sum()
                st.metric("Textos Válidos", nonEmptyTexts)
            with col3:
                emptyTexts = len(dataset) - nonEmptyTexts
                st.metric("Textos Vazios", emptyTexts)

            # Show sample texts
            st.markdown("**Exemplos de textos na coluna selecionada:**")
            sampleTexts = dataset[selectedTextColumn].dropna().head(5)
            for i, text in enumerate(sampleTexts, 1):
                st.write(f"{i}. {str(text)[:100]}...")

            st.success(f"✅ Arquivo '{uploadedFile.name}' carregado com sucesso e coluna alvo selecionada: {selectedTextColumn}")

st.markdown("---")

# =============================================================================
# Step 3: Model Selection
# =============================================================================

st.markdown("### Etapa 3: Seleção do Modelo")
st.markdown("Escolha um modelo do Hugging Face para classificação de texto.")

# Default model
defaultModel = "distilbert-base-uncased-finetuned-sst-2-english"

# Check if model is loaded
modelLoaded = (st.session_state.currentTaskInEdition.model is not None and
                st.session_state.currentTaskInEdition.tokenizer is not None)

# Field with current or default value (disabled if model is loaded)
modelId = st.text_input(
    "Digite o ID do modelo do Hugging Face:",
    value=st.session_state.currentTaskInEdition.modelID or defaultModel,
    placeholder="Ex: distilbert-base-uncased-finetuned-sst-2-english",
    help="Você pode encontrar modelos em: https://huggingface.co/models" if not modelLoaded else "Campo desabilitado - modelo carregado. Use o botão 'Remover Modelo' para editar.",
    disabled=modelLoaded
)

# Update model ID in task (only if not disabled)
if not modelLoaded:
    st.session_state.currentTaskInEdition.SetModelID(modelId.strip() or None)

# Buttons layout
col1, col2 = st.columns([1, 1])

with col1:
    # Button to load model (disabled if already loaded)
    load_button = st.button(
        "📥 Carregar Modelo",
        use_container_width=True,
        disabled=modelLoaded
    )

with col2:
    # Button to remove loaded model (only visible if model is loaded)
    remove_button = st.button(
        "🗑️ Remover Modelo",
        use_container_width=True,
        disabled=not modelLoaded,
        help="Remove o modelo atual da memória para carregar outro"
    )

# Handle remove model button
if remove_button and modelLoaded:
    # Clear model from memory
    st.session_state.currentTaskInEdition.model = None
    st.session_state.currentTaskInEdition.tokenizer = None
    st.session_state.currentTaskInEdition.pipeline = None
    st.session_state.currentTaskInEdition.SetModelID(None)

    st.success("🗑️ Modelo removido da memória com sucesso!")
    st.info("💡 Agora você pode carregar um novo modelo.")
    st.rerun()

# Handle load model button
if load_button and not modelLoaded:
    if modelId and modelId.strip():
        # Create terminal output
        st.markdown("#### 💻 Terminal de Carregamento")
        terminalOutput = st.empty()

        # Initial messages
        terminalMessages = [
            f"🔄 Iniciando download do modelo: {modelId.strip()}",
            "⏳ Preparando ambiente..."
        ]

        # Callback function to update terminal
        def UpdateProgressCallback(step, message):
            # Update terminal messages
            if step == 1:
                terminalMessages.append("🔍 Verificando disponibilidade do modelo... ✅")
            elif step == 2:
                terminalMessages.append("📦 Iniciando download do tokenizer...")
            elif step == 3:
                terminalMessages.append("📦 Tokenizer baixado com sucesso ✅")
            elif step == 4:
                terminalMessages.append("🤖 Iniciando download do modelo...")
                terminalMessages.append("⏳ Isso pode demorar alguns minutos dependendo do tamanho do modelo...")
            elif step == 5:
                terminalMessages.append("🤖 Modelo baixado com sucesso ✅")
            elif step == 6:
                terminalMessages.append(f"💻 {message}")
            elif step == 7:
                terminalMessages.append("⚙️ Configurando pipeline de classificação...")
            elif step == 8:
                terminalMessages.append("⚙️ Pipeline configurado com sucesso ✅")
            elif step == 9:
                terminalMessages.append("🧪 Executando teste de funcionalidade...")
            elif step == 10:
                terminalMessages.append("🧪 Teste concluído com sucesso ✅")
                terminalMessages.append("🎉 Carregamento finalizado!")

            # Update terminal display
            terminalOutput.code("\n".join(terminalMessages), language="bash")

        # Display initial terminal state
        terminalOutput.code("\n".join(terminalMessages), language="bash")

        # Try to load the model with progress callback
        success, message = st.session_state.currentTaskInEdition.LoadModel(
            progress_callback = UpdateProgressCallback
        )

        # Update terminal with final result
        if success:
            finalMessages = terminalMessages + [
                "",
                "=" * 50,
                message,
                "=" * 50
            ]
        else:
            finalMessages = terminalMessages + [
                "",
                "❌ ERRO DURANTE O CARREGAMENTO:",
                message,
                "",
                "💡 Sugestões:",
                "- Verifique se o ID do modelo está correto",
                "- Tente um modelo diferente",
                "- Verifique sua conexão com a internet",
                "- Alguns modelos podem não estar disponíveis"
            ]

        terminalOutput.code("\n".join(finalMessages), language="bash")
    else:
        st.error("⚠️ Digite um ID de modelo válido")

# Verify if model was loaded (update status after operations)
modelLoaded = (st.session_state.currentTaskInEdition.model is not None and
               st.session_state.currentTaskInEdition.tokenizer is not None)

if modelLoaded:
        # Show model information
        st.markdown("#### Informações do Modelo")

        modelInfo = st.session_state.currentTaskInEdition.GetModelInfo()

        infoColumn1, infoColumn2, infoColumn3, infoColumn4, infoColumn5 = st.columns(5)

        with infoColumn1:
            st.metric("🤖 Tipo", modelInfo.get("model_type", "N/A"))

        with infoColumn2:
            st.metric("📝 Vocabulário", f"{modelInfo.get('vocab_size', 0):,}")

        with infoColumn3:
            st.metric("📏 Tamanho Máximo", modelInfo.get('max_length', 0))

        with infoColumn4:
            st.metric("🏷️ Classes", modelInfo.get('num_labels', 'N/A'))

        # Performance indicator
        device = modelInfo.get('device', 'CPU')
        if device == 'GPU':
            st.success("💡 Executando em GPU 🚀")
        else:
            st.info("💡 Executando em CPU 🐌")

        # Quick test
        st.markdown("#### 🧪 Teste Rápido")

        # Layout with text input and button side by side
        col_text, col_button = st.columns([4, 1])

        with col_text:
            testText = st.text_input(
                "Digite um texto para testar o modelo:",
                placeholder="Este produto é muito bom!",
                label_visibility="visible"
            )

        with col_button:
            st.markdown("<div style='margin-top: 29px;'></div>", unsafe_allow_html=True)  # Align button with text input
            test_button = st.button("🔍 Testar", key="test_model", use_container_width=True)

        if testText and test_button:
            try:
                with st.spinner("Processando..."):
                    results = st.session_state.currentTaskInEdition.pipeline(testText)

                st.markdown("**Resultado:**")
                for result in results[0]:
                    label = result['label']
                    score = result['score']
                    st.write(f"- **{label}**: {score:.3f} ({score*100:.1f}%)")

            except Exception as e:
                st.error(f"❌ Erro no teste: {str(e)}")

        st.success("✅ Modelo carregado com sucesso!")

else:
    if modelId.strip():
        st.warning("⚠️ Carregue o modelo para continuar")
    else:
        st.info("💡 Digite o ID de um modelo e clique em 'Carregar Modelo'")

st.markdown("---")

# =============================================================================
# Step 4: Configuration and Execution
# =============================================================================

st.markdown("### Etapa 4: Configuração e Execução")
st.markdown("Configure e execute a classificação de texto no seu dataset.")

# Info about save and download options
st.info("💡 **Opções de Saída**: O arquivo será salvo localmente no diretório especificado e também estará disponível para download em múltiplos formatos após a execução.")
st.markdown("")

# Check if required components are available
currentTask = st.session_state.currentTaskInEdition
hasDataset = currentTask.inputDataset is not None
hasModel = currentTask.pipeline is not None

if not hasDataset:
    st.error("❌ Dataset não carregado. Volte para a Etapa 2.")
    st.stop()

if not hasModel:
    st.error("❌ Modelo não carregado. Volte para a Etapa 3.")
    st.stop()

# Check if text column was selected in Step 2
if 'selectedTextColumn' not in st.session_state or st.session_state.selectedTextColumn is None:
    st.error("❌ Coluna de texto não selecionada. Volte para a Etapa 2.")
    st.stop()

selectedTextColumn = st.session_state.selectedTextColumn

# Verify column still exists in dataset
if selectedTextColumn not in currentTask.inputDataset.columns:
    st.error("❌ A coluna selecionada não existe mais no dataset. Volte para a Etapa 2.")
    st.stop()

# Default path suggestions
defaultPaths = [
    str(pathlib.Path.home() / "Desktop"),
    str(pathlib.Path.home() / "Documents"),
    str(pathlib.Path.home() / "Downloads"),
]

# Initialize output settings in session state if not exists
if 'outputDirectory' not in st.session_state:
    st.session_state.outputDirectory = defaultPaths[0]
if 'outputFileName' not in st.session_state:
    st.session_state.outputFileName = ""
if 'outputFormat' not in st.session_state:
    st.session_state.outputFormat = "csv"

# Get current suggested path
currentSuggestion = st.session_state.outputDirectory

# Create columns for text input and buttons
textCol, btn1Col, btn2Col, btn3Col = st.columns([8.5, 0.5, 0.5, 0.5])

with textCol:
    outputDirectory = st.text_input(
        label="Diretório de Saída:",
        value=currentSuggestion,
        placeholder="Ex: C:/Users/usuario/Desktop/resultados/",
        help="Diretório onde o arquivo classificado será salvo",
    )

with btn1Col:
    # Adiciona um pequeno espaço no topo para alinhar
    st.markdown("<div style='margin-top: 27px;'></div>", unsafe_allow_html=True)
    if st.button("📋", help="Desktop", use_container_width=True, key="desktop_btn"):
        st.session_state.outputDirectory = defaultPaths[0]
        st.rerun()

with btn2Col:
    st.markdown("<div style='margin-top: 27px;'></div>", unsafe_allow_html=True)
    if st.button("📁", help="Documentos", use_container_width=True, key="docs_btn"):
        st.session_state.outputDirectory = defaultPaths[1]
        st.rerun()

with btn3Col:
    st.markdown("<div style='margin-top: 27px;'></div>", unsafe_allow_html=True)
    if st.button("⬇️", help="Downloads", use_container_width=True, key="downloads_btn"):
        st.session_state.outputDirectory = defaultPaths[2]
        st.rerun()

# Update output directory in session state
st.session_state.outputDirectory = outputDirectory

# Create two columns for file name and format
nameCol, formatCol = st.columns([8.5, 1.5])

with nameCol:
    # Default file name with timestamp and task info
    taskName = currentTask.taskName or "classificacao_texto"
    # Clean task name for filename (remove special characters)
    cleanTaskName = "".join(c for c in taskName if c.isalnum() or c in (' ', '-', '_')).rstrip()
    cleanTaskName = cleanTaskName.replace(' ', '_').lower()
    defaultFileName = f"{cleanTaskName}_{datetime.now().strftime('%d-%m-%Y')}"

    outputFileName = st.text_input(
        "Nome do arquivo (sem extensão):",
        value=st.session_state.outputFileName or defaultFileName,
        placeholder=defaultFileName,
        help="Digite o nome desejado para o arquivo classificado"
    )

    # Update output file name in session state
    st.session_state.outputFileName = outputFileName

with formatCol:
    # File format selector
    outputFormat = st.selectbox(
        "Formato do arquivo:",
        options=['csv', 'xlsx', 'json', 'parquet'],
        index=['csv', 'xlsx', 'json', 'parquet'].index(st.session_state.outputFormat),
        help="Escolha o formato de exportação dos dados classificados"
    )

    # Update output format in session state
    st.session_state.outputFormat = outputFormat

# Show preview of full file name
if outputFileName.strip():
    fullFileName = f"{outputFileName.strip()}.{outputFormat}"
    st.info(f"� **Arquivo local**: {fullFileName} | 📥 **Downloads**: Disponíveis em múltiplos formatos após execução")

# Check if configuration is complete
if outputDirectory.strip() and outputFileName.strip():
    st.success("✅ Configuração de saída concluída!")
else:
    st.warning("⚠️ Preencha todos os campos para continuar.")

# Initialize session state for execution
if 'isExecuting' not in st.session_state:
    st.session_state.isExecuting = False
if 'executionResults' not in st.session_state:
    st.session_state.executionResults = None

# Execution button
st.markdown("#### Execução")

# Get configuration from session state
outputDirectory = st.session_state.outputDirectory
outputFileName = st.session_state.outputFileName
outputFormat = st.session_state.outputFormat

canExecute = (selectedTextColumn and
              outputDirectory.strip() and
              outputFileName.strip() and
              not st.session_state.isExecuting)

executeButton = st.button(
    "▶️ Iniciar Classificação",
    disabled=not canExecute,
    use_container_width=True,
    help="Inicia o processo de classificação de todo o dataset" if canExecute else "Complete a configuração de saída para continuar"
)

# Stop execution button (only visible during execution)
if st.session_state.isExecuting:
    if st.button("⏹️ Parar Execução", use_container_width=True, type="secondary"):
        st.session_state.isExecuting = False
        st.warning("⚠️ Execução interrompida pelo usuário.")
        st.rerun()

# Execute classification
if executeButton and canExecute:
    st.session_state.isExecuting = True

    # Validate output directory
    try:
        # Normalize path
        outputDirectory = os.path.normpath(outputDirectory.strip())

        # Create directory if it doesn't exist
        if not os.path.exists(outputDirectory):
            os.makedirs(outputDirectory, exist_ok=True)

        # Create output file path with user-defined name and format
        fullFileName = f"{outputFileName.strip()}.{outputFormat}"
        outputFilePath = os.path.join(outputDirectory, fullFileName)

        # Test write permissions
        testFile = os.path.join(outputDirectory, "test_write.tmp")
        try:
            with open(testFile, 'w') as f:
                f.write("test")
            os.remove(testFile)
        except PermissionError:
            raise Exception(f"Sem permissão de escrita no diretório: {outputDirectory}")

    except Exception as e:
        st.error(f"❌ Erro ao configurar diretório de saída: {str(e)}")
        st.session_state.isExecuting = False
        st.stop()

    # Create progress containers
    progressBar = st.progress(0, text="Progresso: 0%")
    terminalContainer = st.empty()

    # Initialize progress tracking
    terminalMessages = [
        "🚀 Iniciando classificação de texto...",
        f"📊 Dataset: {len(currentTask.inputDataset)} linhas",
        f"📝 Coluna de texto: {selectedTextColumn}",
        f"🤖 Modelo: {currentTask.modelID}",
        f"💾 Saída: {outputFilePath}",
        "",
        "⏳ Processando..."
    ]

    # Progress callback function
    def progressCallback(currentRow, totalRows, lastLabel):
        percentage = (currentRow / totalRows) * 100
        # Update only a single progress bar for the whole process
        progressBar.progress(percentage / 100, text=f"Progresso: {percentage:.1f}%")
        # Update terminal messages every 50 rows or at the end
        if currentRow % 50 == 0 or currentRow == totalRows:
            terminalMessages.append(f"✅ Processadas {currentRow:,}/{totalRows:,} linhas ({percentage:.1f}%)")
            terminalContainer.code("\n".join(terminalMessages), language="bash")

    # Display initial progress
    terminalContainer.code("\n".join(terminalMessages), language="bash")

    # Start classification task
    currentTask.StartExecution()

    # Execute classification
    success, message = currentTask.ExecuteClassification(
        textColumn=selectedTextColumn,
        progressCallback=progressCallback
    )

    # Save results if successful
    if success and currentTask.outputDataset is not None:
        try:
            # Save in the selected format
            if outputFormat == 'csv':
                currentTask.outputDataset.to_csv(outputFilePath, index=False)
            elif outputFormat == 'xlsx':
                currentTask.outputDataset.to_excel(outputFilePath, index=False, engine='openpyxl')
            elif outputFormat == 'json':
                currentTask.outputDataset.to_json(outputFilePath, orient='records', indent=2)
            elif outputFormat == 'parquet':
                currentTask.outputDataset.to_parquet(outputFilePath, index=False)

            currentTask.SetOutputDatasetPath(outputFilePath)
            currentTask.CompleteTask(outputFilePath)

            finalMessages = terminalMessages + [
                "",
                "=" * 50,
                "✅ CLASSIFICAÇÃO CONCLUÍDA COM SUCESSO!",
                f"📁 Arquivo salvo em: {outputFilePath}",
                f"📊 Total de linhas processadas: {len(currentTask.outputDataset):,}",
                f"📄 Formato do arquivo: {outputFormat.upper()}",
                "=" * 50
            ]

            st.session_state.executionResults = {
                'success': True,
                'outputPath': outputFilePath,
                'totalRows': len(currentTask.outputDataset),
                'outputFormat': outputFormat
            }

        except Exception as saveError:
            success = False
            message = f"❌ Erro ao salvar arquivo: {str(saveError)}"
            finalMessages = terminalMessages + [
                "",
                "❌ ERRO AO SALVAR RESULTADO:",
                str(saveError),
                "",
                "💡 Possíveis soluções:",
                "- Verifique as permissões do diretório",
                "- Tente um formato de arquivo diferente",
                "- Certifique-se de que o arquivo não está aberto em outro programa"
            ]

            st.session_state.executionResults = {
                'success': False,
                'error': str(saveError)
            }
    else:
        currentTask.FailTask(message)
        finalMessages = terminalMessages + [
            "",
            "❌ ERRO DURANTE A CLASSIFICAÇÃO:",
            message
        ]

        st.session_state.executionResults = {
            'success': False,
            'error': message
        }

    # Update final terminal display
    terminalContainer.code("\n".join(finalMessages), language="bash")

    # Update execution state
    st.session_state.isExecuting = False

# Show execution results
if st.session_state.executionResults:
    results = st.session_state.executionResults

    if results['success']:

        st.markdown("---")
        # Show results summary
        st.markdown("#### Resumo dos Resultados")

        if currentTask.outputDataset is not None:
            # Create two columns for results and download options
            resultsCol, downloadCol = st.columns([2, 1])

            with resultsCol:
                # Show sample results with all probability columns
                st.markdown("**Amostra dos Resultados:**")

                # Get all probability columns (columns starting with 'prob_')
                prob_columns = [col for col in currentTask.outputDataset.columns if col.startswith('prob_')]

                # Select columns to show in sample
                display_columns = [selectedTextColumn, 'predicted_label', 'confidence_score'] + prob_columns
                available_columns = [col for col in display_columns if col in currentTask.outputDataset.columns]

                sampleResults = currentTask.outputDataset[available_columns].head(10)
                st.dataframe(sampleResults, use_container_width=True)

                # Show information about probability columns
                if prob_columns:
                    st.info(f"💡 **Colunas de Probabilidade**: O modelo retornou probabilidades para {len(prob_columns)} classes: {', '.join([col.replace('prob_', '') for col in prob_columns])}")

            with downloadCol:
                st.markdown("**Opções de Download:**")

                # Get the base filename without extension
                base_filename = st.session_state.outputFileName or f"classificacao_{datetime.now().strftime('%d%m%Y_%H%M%S')}"

                # Download buttons for different formats
                for format_type in ['csv', 'xlsx', 'json', 'parquet']:
                    try:
                        download_data, filename, mime_type = generate_download_data(
                            currentTask.outputDataset,
                            format_type,
                            base_filename
                        )

                        format_icons = {
                            'csv': '📊',
                            'xlsx': '📈',
                            'json': '📋',
                            'parquet': '🗃️'
                        }

                        st.download_button(
                            label=f"{format_icons.get(format_type, '📄')} Download {format_type.upper()}",
                            data=download_data,
                            file_name=filename,
                            mime=mime_type,
                            use_container_width=True,
                            help=f"Baixar dados classificados em formato {format_type.upper()}"
                        )
                    except Exception as e:
                        st.error(f"Erro ao gerar {format_type}: {str(e)}")

                # Additional information
                st.markdown("---")
                st.markdown("**Informações do Arquivo:**")
                st.metric("Total de Linhas", f"{len(currentTask.outputDataset):,}")
                st.metric("Total de Colunas", len(currentTask.outputDataset.columns))

                # Show file size estimate
                memory_usage_mb = currentTask.outputDataset.memory_usage(deep=True).sum() / (1024 * 1024)
                st.metric("Tamanho Estimado", f"{memory_usage_mb:.1f} MB")

                # Show where the file was saved locally
                if 'outputPath' in results:
                    st.markdown("**Arquivo Local:**")
                    st.success(f"💾 Salvo em:\n`{results['outputPath']}`")

    else:
        st.error(f"❌ Erro na execução: {results['error']}")

st.markdown("---")

# =============================================================================
# Final Status
# =============================================================================

# =============================================================================
# Rodapé
# =============================================================================

st.markdown("### Sobre esta Tarefa")

infoColumn1, infoColumn2 = st.columns(2)

with infoColumn1:
    st.markdown("""
    **Classificação de Texto** é uma tarefa fundamental de Machine Learning que permite:

    - 📍 **Análise de Sentimento**: Determinar se um texto é positivo, negativo ou neutro
    - 🏷️ **Categorização**: Classificar textos em categorias predefinidas
    - 🔍 **Detecção de Spam**: Identificar mensagens indesejadas
    - 🎯 **Classificação de Tópicos**: Organizar documentos por assunto
    """)


st.markdown("---")
with infoColumn2:
    st.markdown("""
    **Modelos Recomendados:**

    - 🌟 **BERT**: Excelente para análise de sentimento
    - ⚡ **DistilBERT**: Versão mais rápida do BERT
    - 🌍 **Multilingual**: Para textos em português
    - 🎯 **Fine-tuned**: Modelos específicos para suas necessidades
    """)

st.markdown("---")
