import sqlite3
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import platform

def load_data_from_db(db_path):
    """
    데이터베이스에서 seoul_analysis_data 테이블의 모든 데이터를 불러와 
    Pandas DataFrame으로 반환합니다.
    Retrieves all data from the seoul_analysis_data table 
    in the database and returns it as a Pandas DataFrame.
    """
    try:
        # DB 연결 및 쿼리 실행
        conn = sqlite3.connect(db_path)
        query = "SELECT * FROM seoul_analysis_data"
        df = pd.read_sql_query(query, conn)
        conn.close()
        print(f"Success! Loaded {len(df)} rows.")
        
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def analyze_price_by_age_and_district(df):
    """
    자치구명과 신축 여부별 평당 가격 평균을 계산하고 출력합니다.
    Calculate and output the average price per square meter 
    by autonomous district name and whether the building is newly constructed.
    """
    if df is None:
        return
    
    # 그룹화 및 평균 계산 (Group and calculate mean)
    grouped_df = df.groupby(['자치구명', 'is_new_building'])['price_per_pyung'].mean().reset_index()
    
    print("\n--- Price Analysis by District and New/Old Status ---")
    # 평당 가격이 높은 순서대로 정렬하고, DataFrame 형태 유지하며 출력
    print(grouped_df.sort_values(by='price_per_pyung', ascending=False).to_string(index=False))
    
    return grouped_df

# ----------------------------------------------------
# 2. MAIN EXECUTION FLOW (스크립트 실행 시 동작)
# ----------------------------------------------------

def main():
    """
    Define the starting point of the program
    """
    DB_PATH = r'/Users/raymondhwang/Downloads/부동산/seoul_analysis.db' 
    
    df_analysis = load_data_from_db(DB_PATH)
    
    if df_analysis is not None:
        print("\n--- Data Info ---")
        df_analysis.info() # 데이터 타입과 결측치 확인 (중요)
        set_korean_font()
        analyze_price_by_age_and_district(df_analysis)
        visualize_new_vs_old(df_analysis)
        
        
def visualize_new_vs_old(df):
    """신축/구축별 가격 분포를 Box Plot으로 시각화"""
    
    plt.figure(figsize=(18, 6))
    
    # Box Plot을 이용해 분포를 시각화 (그룹별 가격의 중간값, 사분위수 확인)
    sns.boxplot(x='자치구명', y='price_per_pyung', hue='is_new_building', data=df)
    
    plt.title('자치구별 신축 vs 구축 평당 가격 분포', fontsize=16)
    plt.xlabel('자치구명', fontsize=12)
    plt.ylabel('평당 가격 (만원)', fontsize=12)
    # plt.xticks(rotation=45)
    plt.legend(title='신축 여부')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()
    
def set_korean_font():
    """시스템에 맞는 한글 폰트 설정"""
    system = platform.system()
    if system == "Darwin":
        plt.rcParams['font.family'] = 'AppleGothic'
    elif system == "Windows":
        plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지


# 스크립트가 직접 실행될 때만 main() 함수 호출
if __name__ == "__main__":
    main()