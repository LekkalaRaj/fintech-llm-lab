"""
Main Gradio application for Synthetic Financial Dataset Generator.
"""
import gradio as gr
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from loguru import logger

from src.config.settings import settings, DOMAINS, EXPORT_FORMATS
from src.llm.gemini_client import GeminiClient
from src.generators.capital_markets import CapitalMarketsGenerator
from src.generators.banking import BankingGenerator
from src.generators.private_equity import PrivateEquityGenerator
from src.generators.venture_capital import VentureCapitalGenerator
from src.utils.data_exporter import DataExporter
from src.utils.metrics_calculator import MetricsCalculator
from src.validators.search_validator import SearchValidator
from src.utils.logger import setup_logger


# Initialize components
try:
    settings.validate_api_keys()
    settings.create_output_dir()
    
    gemini_client = GeminiClient()
    capital_markets_gen = CapitalMarketsGenerator(gemini_client)
    banking_gen = BankingGenerator(gemini_client)
    private_equity_gen = PrivateEquityGenerator(gemini_client)
    venture_capital_gen = VentureCapitalGenerator(gemini_client)
    
    exporter = DataExporter()
    metrics_calc = MetricsCalculator()
    search_validator = SearchValidator()
    
    logger.info("All components initialized successfully")
except Exception as e:
    logger.error(f"Initialization error: {str(e)}")
    raise


def update_dataset_choices(domain: str) -> gr.Dropdown:
    """Update dataset choices based on selected domain."""
    datasets = DOMAINS.get(domain, {}).get("datasets", [])
    return gr.Dropdown(choices=datasets, value=datasets[0] if datasets else None)


def generate_dataset(
    domain: str,
    dataset_type: str,
    num_records: int,
    start_date: str,
    end_date: str,
    format_type: str,
    include_validation: bool,
    progress=gr.Progress()
):
    """
    Main function to generate synthetic dataset.
    
    Args:
        domain: Financial domain
        dataset_type: Type of dataset
        num_records: Number of records to generate
        start_date: Start date for time-series data
        end_date: End date for time-series data
        format_type: Export format
        include_validation: Whether to include Google Search validation
        progress: Gradio progress tracker
    
    Returns:
        Tuple of (dataframe preview, metrics HTML, sources HTML, file path, status message)
    """
    try:
        progress(0, desc="Initializing generation...")
        logger.info(f"Starting generation: {domain} - {dataset_type} - {num_records} records")
        
        # Validate inputs
        if not domain or not dataset_type:
            return None, "", "", None, "❌ Please select domain and dataset type"
        
        if num_records < 10 or num_records > settings.max_records:
            return None, "", "", None, f"❌ Number of records must be between 10 and {settings.max_records}"
        
        # Select appropriate generator
        progress(0.1, desc="Selecting generator...")
        if domain == "Capital Markets":
            generator = capital_markets_gen
        elif domain == "Banking":
            generator = banking_gen
        elif domain == "Private Equity":
            generator = private_equity_gen
        elif domain == "Venture Capital":
            generator = venture_capital_gen
        else:
            return None, "", "", None, f"❌ Generator for {domain} not yet implemented"
        
        # Generate data
        progress(0.2, desc=f"Generating {num_records} records...")
        df = generator.generate(
            dataset_type=dataset_type,
            num_records=num_records,
            start_date=start_date if start_date else None,
            end_date=end_date if end_date else None
        )
        
        if df.empty:
            return None, "", "", None, "❌ Generation failed - no data produced"
        
        progress(0.6, desc="Calculating quality metrics...")
        # Calculate metrics
        metrics = metrics_calc.calculate_all_metrics(df)
        metrics_html = metrics_calc.format_metrics_html(metrics)
        
        # Validation with Google Search
        sources_html = ""
        if include_validation:
            progress(0.7, desc="Validating with Google Search...")
            try:
                sources = search_validator.validate_domain_patterns(domain, dataset_type)
                sources_html = search_validator.format_sources_html(sources)
            except Exception as e:
                logger.warning(f"Search validation failed: {str(e)}")
                sources_html = "<p>⚠️ Search validation unavailable</p>"
        else:
            sources_html = "<p>Search validation was not requested</p>"
        
        progress(0.8, desc=f"Exporting to {format_type}...")
        # Export data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{domain.replace(' ', '_')}_{dataset_type.replace(' ', '_')}_{timestamp}"
        
        filepath = exporter.export(
            df,
            filename=filename,
            format_type=format_type
        )
        
        progress(1.0, desc="Complete!")
        
        # Prepare preview (first 100 rows)
        df_preview = df.head(100)
        
        # Remove metadata columns from preview
        meta_cols = [col for col in df_preview.columns if col.startswith('_meta_') or col.startswith('_generated')]
        df_preview = df_preview.drop(columns=meta_cols, errors='ignore')
        
        success_msg = f"✅ Successfully generated {len(df)} records and exported to {filepath.name}"
        logger.info(success_msg)
        
        return df_preview, metrics_html, sources_html, str(filepath), success_msg
        
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        logger.error(f"Generation failed: {str(e)}", exc_info=True)
        return None, "", "", None, error_msg


def validate_with_search(domain: str, dataset_type: str):
    """
    Perform validation search without generating data.
    
    Args:
        domain: Financial domain
        dataset_type: Dataset type
    
    Returns:
        HTML with validation sources
    """
    try:
        if not domain or not dataset_type:
            return "<p>Please select domain and dataset type first</p>"
        
        logger.info(f"Performing validation search for {domain} - {dataset_type}")
        sources = search_validator.validate_domain_patterns(domain, dataset_type)
        
        if sources:
            return search_validator.format_sources_html(sources)
        else:
            return "<p>⚠️ No validation sources found. This could be due to rate limiting or API issues.</p>"
            
    except Exception as e:
        logger.error(f"Validation search failed: {str(e)}")
        return f"<p>❌ Validation failed: {str(e)}</p>"


# Build Gradio Interface
def build_interface():
    """Build and configure Gradio interface."""
    
    with gr.Blocks(
        title="Synthetic Financial Dataset Generator",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {font-family: 'Arial', sans-serif;}
        .header {text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 20px;}
        .info-box {background-color: #e7f3ff; padding: 15px; border-radius: 8px; border-left: 4px solid #2196F3; margin: 10px 0;}
        """
    ) as app:
        
        # Header
        gr.HTML("""
        <div class="header">
            <h1>🏦 Synthetic Financial Dataset Generator</h1>
            <p>Generate realistic synthetic datasets for Capital Markets, Private Equity, VC, and Banking domains</p>
            <p style="font-size: 0.9em; opacity: 0.9;">Powered by Google Gemini LLM with Google Search Validation</p>
        </div>
        """)
        
        # Info box
        gr.HTML("""
        <div class="info-box">
            <strong>ℹ️ About:</strong> This application generates synthetic financial datasets using AI. 
            All data is completely artificial and does not contain any real customer information. 
            Data patterns are validated against real-world sources using Google Search.
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 📋 Configuration")
                
                domain = gr.Dropdown(
                    choices=list(DOMAINS.keys()),
                    label="Financial Domain",
                    value=list(DOMAINS.keys())[0],
                    info="Select the financial domain"
                )
                
                dataset_type = gr.Dropdown(
                    choices=DOMAINS[list(DOMAINS.keys())[0]]["datasets"],
                    label="Dataset Type",
                    info="Select the type of dataset to generate"
                )
                
                num_records = gr.Slider(
                    minimum=10,
                    maximum=10000,
                    value=1000,
                    step=10,
                    label="Number of Records",
                    info="Number of records to generate"
                )
                
                with gr.Row():
                    start_date = gr.Textbox(
                        label="Start Date (YYYY-MM-DD)",
                        value=(datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"),
                        info="For time-series data"
                    )
                    
                    end_date = gr.Textbox(
                        label="End Date (YYYY-MM-DD)",
                        value=datetime.now().strftime("%Y-%m-%d"),
                        info="For time-series data"
                    )
                
                format_type = gr.Dropdown(
                    choices=list(EXPORT_FORMATS.keys()),
                    label="Export Format",
                    value="CSV",
                    info="Choose output format"
                )
                
                include_validation = gr.Checkbox(
                    label="Include Google Search Validation",
                    value=True,
                    info="Cross-reference with real-world data patterns"
                )
                
                with gr.Row():
                    generate_btn = gr.Button("🚀 Generate Dataset", variant="primary", size="lg")
                    validate_btn = gr.Button("🔍 Validate Only", variant="secondary")
            
            with gr.Column(scale=2):
                gr.Markdown("### 📊 Results")
                
                status_msg = gr.Textbox(
                    label="Status",
                    interactive=False,
                    show_label=False
                )
                
                with gr.Tabs():
                    with gr.Tab("📄 Data Preview"):
                        data_preview = gr.Dataframe(
                            label="Generated Data (first 100 rows)",
                            interactive=False,
                            wrap=True
                        )
                    
                    with gr.Tab("📈 Quality Metrics"):
                        metrics_output = gr.HTML(label="Data Quality Metrics")
                    
                    with gr.Tab("🔗 Validation Sources"):
                        sources_output = gr.HTML(label="Google Search Validation Sources")
                
                download_file = gr.File(
                    label="📥 Download Complete Dataset",
                    interactive=False
                )
        
        # Event handlers
        domain.change(
            fn=update_dataset_choices,
            inputs=[domain],
            outputs=[dataset_type]
        )
        
        generate_btn.click(
            fn=generate_dataset,
            inputs=[
                domain,
                dataset_type,
                num_records,
                start_date,
                end_date,
                format_type,
                include_validation
            ],
            outputs=[
                data_preview,
                metrics_output,
                sources_output,
                download_file,
                status_msg
            ]
        )
        
        validate_btn.click(
            fn=validate_with_search,
            inputs=[domain, dataset_type],
            outputs=[sources_output]
        )
        
        # Footer
        gr.HTML("""
        <div style="text-align: center; padding: 20px; margin-top: 30px; border-top: 1px solid #ddd;">
            <p style="color: #666; font-size: 0.9em;">
                <strong>⚠️ Disclaimer:</strong> This tool generates synthetic data for development and testing purposes only. 
                All generated data is completely artificial and should not be used for actual financial decisions.
            </p>
            <p style="color: #999; font-size: 0.8em;">
                Powered by Google Gemini | Built with Gradio | Version 1.0.0
            </p>
        </div>
        """)
    
    return app


def main():
    """Main entry point."""
    try:
        logger.info("Starting Synthetic Financial Dataset Generator")
        
        # Test Gemini connection
        if not gemini_client.test_connection():
            logger.error("Failed to connect to Gemini API")
            raise Exception("Gemini API connection failed. Please check your API key.")
        
        # Build and launch app
        app = build_interface()
        
        app.launch(
            server_name=settings.gradio_server_name,
            server_port=settings.gradio_server_port,
            share=settings.gradio_share,
            show_error=True
        )
        
    except Exception as e:
        logger.error(f"Application failed to start: {str(e)}")
        raise


if __name__ == "__main__":
    main()